# fastapi imports
from fastapi import FastAPI, APIRouter, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.concurrency import asynccontextmanager
from fastapi_utils.tasks import repeat_every

# python imports
import os
import time
import asyncio
import json

# local imports
from src.config import config

# route imports
from src.routes.main import main as main_route
from src.routes.auth import auth as auth_route
from src.routes.bot import bot as bot_route
from src.routes.upload import upload as upload_route

# schema imports
from src.schemas.announcement import Announcement
from src.schemas.FileTypeException import FileTypeException

# utils imports
from src.utils.remove_old_uploads import remove_expired_files

# 3rd party imports
from datetime import datetime, timedelta
