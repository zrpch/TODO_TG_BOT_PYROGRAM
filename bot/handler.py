import logging

from pyrogram.client import Client
from pyrogram.types import CallbackQuery, Message

from bot.keyboards import Buttons, InlineButtons, InlineKeyboards, Keyboards
from bot.messages import Messages
from bot.states import Keys, States
from cache.cache import Cache
from database.database import Database

db = Database()
cache = Cache()


class TaskHandler:
    """Handles text messages and user interactions in the chat."""

    def __init__(self, client: Client) -> None:
        self.client = client

    async def handle_updates(self, client: Client, message: Message) -> None:
        pass


class CallbackHandler:
    """Handles inline button interactions."""

    def __init__(self, client: Client) -> None:
        self.client = client

    async def handle_callback(self, client: Client, callback_query: CallbackQuery) -> None:
        """Processes inline button clicks."""
        pass
