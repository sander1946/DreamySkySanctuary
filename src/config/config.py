import os
import dotenv

VERSION: str = '0.0.1'
APP_NAME: str = 'DreamySkySanctuary'
DESCRIPTION: str = 'The website of the Dreamy Sky Sanctuary, a discord server about the game Sky: Children of the Light.'

BASE_DIR: str = os.getcwd()
TEMPLATES_DIR: str = os.path.join(BASE_DIR, "templates")
PUBLIC_DIR: str = os.path.join(BASE_DIR, "public")
STATIC_DIR: str = os.path.join(BASE_DIR, "static")
UPLOAD_DIR: str = os.path.join(BASE_DIR, "upload")

UPLOAD_EXPIRE_TIME: int = 60 * 60 * 24 * 31  # 31 days / 1 month

ENV_FILE: str = os.path.join(BASE_DIR, ".env")
TOKEN: str = dotenv.get_key(ENV_FILE, "DISCORD_TOKEN")

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