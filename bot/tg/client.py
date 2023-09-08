from enum import Enum

import requests

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse
from todolist import settings

import logging

logging.basicConfig(filename='bot.log', level=logging.INFO)

class Command(str, Enum):
    GET_UPDATES = 'getUpdates'
    SEND_MESSAGE = 'sendMessage'


class TgClient:
    def __init__(self, token: str | None = None):
        self.token = token if token else settings.BOT_TOKEN

    def get_url(self, method: str) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get(Command.GET_UPDATES, offset=offset, timeout=timeout)
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        data = self._get(Command.SEND_MESSAGE, chat_id=chat_id, text=text)
        return SendMessageResponse(**data)

    def _get(self, command: Command, **params) -> dict:
        url = self.get_url(command.value)
        response = requests.get(url, params=params)
        if not response.ok:
            print(response.json())
            raise ValueError
        return response.json()
