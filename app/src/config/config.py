from datetime import timedelta
import os
import dotenv

VERSION: str = '0.0.1'
APP_NAME: str = 'DreamySkySanctuary'
DESCRIPTION: str = 'The website of the Dreamy Sky Sanctuary, a discord server about the game Sky: Children of the Light.'

CLIENT_ORIGIN: list[str] = [
    "http://localhost",
    "http://dreamyskysanctuary.com",
]

BASE_DIR: str = os.getcwd()
TEMPLATES_DIR: str = os.path.join(BASE_DIR, "templates")
PUBLIC_DIR: str = os.path.join(BASE_DIR, "public")
STATIC_DIR: str = os.path.join(BASE_DIR, "static")
UPLOAD_DIR: str = os.path.join(BASE_DIR, "upload")

UPLOAD_EXPIRE_TIME: int = 60 * 60 * 24 * 31  # 31 days / 1 month
TEAM_EXPIRE_TIME: int = 60 * 60 * 2 # 24 hours / 1 day
ACCESS_TOKEN_EXPIRE_MINUTES: timedelta = timedelta(hours=6)
CHECK_INTERVAL: int = 60 * 60 * 24  # 24 hours


ENV_FILE: str = os.path.join(BASE_DIR, ".env")
TOKEN: str = dotenv.get_key(ENV_FILE, "DISCORD_TOKEN")

SERVER_SECRET: str = dotenv.get_key(ENV_FILE, "SERVER_SECRET")
ALGORITHM: str = "HS256"
OTP_WINDOW: int = 2

DISCORD_OWNER_ID: int = dotenv.get_key(ENV_FILE, "DISCORD_OWNER_ID")

SMTP_SERVER: str = dotenv.get_key(ENV_FILE, "SMTP_SERVER")
SMTP_PORT: int = dotenv.get_key(ENV_FILE, "SMTP_PORT")
SMTP_USERNAME: str = dotenv.get_key(ENV_FILE, "SMTP_USERNAME")
SMTP_PASSWORD: str = dotenv.get_key(ENV_FILE, "SMTP_PASSWORD")


ALLOWED_FILE_TYPES: dict[str, str] = {
    "image/jpeg": "jpg", 
    "image/jpg": "jpg", 
    "image/png": "png", 
    "image/gif": "gif",	
    "image/gifv": "gifv",
    "video/webm": "webm",
    "video/mp4": "mp4",
    "video/wav": "wav",
    "audio/mp3": "mp3",
    "video/ogg": "ogg",}