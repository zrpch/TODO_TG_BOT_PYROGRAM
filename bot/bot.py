import os

from dotenv import load_dotenv
from pyrogram.client import Client
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.sync import idle

from bot.handler import CallbackHandler, TaskHandler
from bot.messages import Messages

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

if not all([BOT_TOKEN, API_ID, API_HASH]):
    raise ValueError(Messages.MISSING_API_CREDENTIALS)

app = Client(name="bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, workdir="sessions")  # type: ignore

task_handler = TaskHandler(app)
callback_handler = CallbackHandler(app)

app.add_handler(MessageHandler(task_handler.handle_updates))
app.add_handler(CallbackQueryHandler(callback_handler.handle_callback))

app.start()  # type: ignore
idle()
app.stop()  # type: ignore
