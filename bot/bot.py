import os

from dotenv import load_dotenv
from pyrogram.client import Client
from pyrogram.sync import idle

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

app = Client(name="bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, workdir="sessions")  # type: ignore

app.start()  # type: ignore
idle()
app.stop()  # type: ignore
