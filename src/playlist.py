import os
from dotenv import load_dotenv
from pathlib import Path
import isodate
from datetime import timedelta
from googleapiclient.discovery import build


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        load_dotenv(Path(Path(__file__).parent.parent, '.env'))
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.playlist_videos = (
            self.youtube.playlistItems()
            .list(
                playlistId=self.playlist_id,
                part='contentDetails,snippet',
                maxResults=50,
            )
            .execute()
        )

    @property
    def channel_id(self):
        return self.playlist_videos['items'][0]['snippet']['channelId']

    @property
    def playlist(self):
        return self.youtube.playlists().list(channelId=self.channel_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()

    @property
    def title(self):
        for pl_list in self.playlist['items']:
            if pl_list['id'] == self.playlist_id:
                return pl_list['snippet']['title']

    @property
    def url(self):
        return 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @property
    def total_duration(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_responce = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        total = timedelta(hours=0, seconds=0)
        for video in video_responce['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration

        return total

    def show_best_video(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_responce = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        vid = None
        max_like = 0
        for video in video_responce['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like:
                max_like = like_count
                vid = video

        return 'https://youtu.be/' + vid['id']
