from src.channel import Channel


class Video:

    def __init__(self, video_id):
        self.video_id = video_id
        self.youtube = Channel.get_service()
        response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.title: str = response['items'][0]['snippet']['title']
        self.url: str = 'https://www.youtube.com/watch?v=' + self.video_id
        self.view_count: int = response['items'][0]['statistics']['viewCount']
        self.like_count: int = response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return super().__str__()




