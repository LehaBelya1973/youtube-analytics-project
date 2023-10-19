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
        self.channel = self.youtube().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channel_id = channel_id


    def print_info(self) -> None | dict:
        """Выводит в консоль информацию о канале."""
        if not self.api_key:
            print("Ключ API YouTube не задан. Установите его в переменных окружения YT_API_KEY.")
            return

        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def title(self):
        return self.print_info()['items'][0]['snippet']['title']

    @property
    def video_count(self):
        return self.print_info()['items'][0]['statistics']['videoCount']

    @property
    def url(self):
        return f"https://www.youtube.com/channel/{self.print_info()['items'][0]['id']}"

    @property
    def channel_id(self):
        return self.__channel_id

    def youtube(self):
        return build('youtube', 'v3', developerKey=self.api_key)
