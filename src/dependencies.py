# fastapi imports
from fastapi import FastAPI, APIRouter, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# local imports
from src.config import config

# route imports
from src.routes.main import main as main_route
from src.routes.auth import auth as auth_route