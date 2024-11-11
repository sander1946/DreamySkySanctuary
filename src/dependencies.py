# fastapi imports
from fastapi import FastAPI, APIRouter, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.concurrency import asynccontextmanager

# python imports
import os
import time
import asyncio

# local imports
from src.config import config

# route imports
from src.routes.main import main as main_route
from src.routes.auth import auth as auth_route
from src.routes.bot import bot as bot_route

# schema imports
from src.schemas.announcement import Announcement

# 3rd party imports
from datetime import datetime, timedelta