import logging

from pyrogram.client import Client
from pyrogram.types import CallbackQuery, Message

from bot.keyboards import Buttons, Keyboards
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
        """Processes user messages and determines the correct action."""
        uid = str(message.chat.id)
        state = cache.get_user_cache(uid, Keys.STATE)
        user = db.get_user(uid)

        if state:
            await self.process_state(uid, state, message)
        else:
            await self.process_command(uid, user, message)

    async def process_state(self, uid: str, state: str, message: Message) -> None:
        """Handles different user states."""
        state_handlers = {
            States.ENTER_NAME: self.register_name,
            States.ENTER_USERNAME: self.register_username,
        }
        if state in state_handlers:
            await state_handlers[state](uid, message)

    async def process_command(self, uid: str, user: object, message: Message) -> None:
        """Handles user commands outside of states."""
        command_handlers = {
            "/start": self.handle_start,
            Buttons.REGISTRATION: self.initiate_registration,
            "/help": self.handle_help,
            Buttons.HELP: self.handle_help,
        }

        handler = command_handlers.get(message.text)
        if handler:
            if handler in [self.handle_start, self.handle_help]:
                await handler(uid, user, message)  # type: ignore
            else:
                await handler(uid, message)  # type: ignore
        else:
            await self.handle_unknown_command(message)

    async def handle_start(self, uid: str, user: object, message: Message) -> None:
        """Handles the /start command."""
        await message.reply(
            Messages.START_REGISTERED if user else Messages.START_NEW,
            reply_markup=Keyboards.MainMenu if user else Keyboards.RegistrationMenu,
        )

    async def handle_help(self, uid: str, user: object, message: Message) -> None:
        """Handles the /help or Help button command."""
        await message.reply(Messages.HELP_TEXT, reply_markup=Keyboards.MainMenu)

    async def handle_unknown_command(self, message: Message) -> None:
        """Handles unknown commands."""
        await message.reply(Messages.UNKNOWN_COMMAND, reply_markup=Keyboards.MainMenu)

    async def initiate_registration(self, uid: str, message: Message) -> None:
        """Starts the registration process."""
        await message.reply(Messages.ENTER_YOUR_NAME)
        cache.update_user_cache(uid, Keys.STATE, States.ENTER_NAME)

    async def register_name(self, uid: str, message: Message) -> None:
        """Processes the user's name during registration."""
        cache.update_user_cache(uid, Keys.NAME, message.text)
        cache.update_user_cache(uid, Keys.STATE, States.ENTER_USERNAME)
        await message.reply(Messages.ENTER_YOUR_USERNAME)

    async def register_username(self, uid: str, message: Message) -> None:
        """Handles username registration and checks if the username is already taken."""
        name = cache.get_user_cache(uid, Keys.NAME)
        username = message.text.strip()

        if db.get_user_by_username(username):
            await message.reply(Messages.USERNAME_EXISTS)
            return

        db.create_user(name, username, uid)
        cache.delete_user_cache(uid)
        await message.reply(Messages.welcome(name), reply_markup=Keyboards.MainMenu)

class CallbackHandler:
    """Handles inline button interactions."""

    def __init__(self, client: Client) -> None:
        self.client = client

    async def handle_callback(self, client: Client, callback_query: CallbackQuery) -> None:
        """Processes inline button clicks."""
        pass
