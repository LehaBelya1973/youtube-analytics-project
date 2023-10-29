import json

import requests
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        load_dotenv()
        self.api_key = os.getenv('YT_API_KEY') # Получаем ключ из переменных окружения
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channel_id = channel_id
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']
        self.url = 'https://www.youtube.com/channel/'+self.__channel_id

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)



    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))


    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        load_dotenv()
        api_key = os.getenv('YT_API_KEY')  # Получаем ключ из переменных окружения
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        data = self.__dict__
        del(data['channel'])
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
