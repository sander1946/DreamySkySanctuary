from src.utils.flash import FlashCategory, flash, get_flashed_messages
from src.utils.refresh_team_file import get_team_data
from src.dependencies import *
from src.schemas.announcement import Announcement
from datetime import datetime, timedelta
from fastapi import status

from src.routes.bot.bot import fetch_by_id

router = APIRouter(
    prefix="",
    tags=["Main"]
)

templates = Jinja2Templates(directory=config.TEMPLATES_DIR)
templates.env.globals["get_flashed_messages"] = get_flashed_messages

@router.get("/", include_in_schema=True)
async def main(request: Request, response: Response):
    user = request.state.user
    response.status_code = status.HTTP_200_OK
    announcements = [
        Announcement(title="Welcome to the API",
        description = "This is a simple API that uses FastAPI and Jinja2 to render HTML templates.",
        author = "Kai",
        date = datetime.now()),
        Announcement(title="This is a test announcement",
        description = "This is a test announcement to show how the announcements are displayed.",
        date = datetime.now() - timedelta(days=1),
        image = "/public/imgs/flags/en.webp"),
    ]    
    
    return templates.TemplateResponse(name="main/main.html", context={"request": request, "user": user, "announcements": announcements})


@router.get("/enchanted", include_in_schema=True)
async def enchanted(request: Request, response: Response):
    response.status_code = status.HTTP_307_TEMPORARY_REDIRECT
    return RedirectResponse("/")


@router.get("/events", include_in_schema=True)
async def events(request: Request, response: Response):
    response.status_code = status.HTTP_307_TEMPORARY_REDIRECT
    return RedirectResponse("/")


@router.get("/memory", include_in_schema=True)
async def enchamemorynted(request: Request, response: Response):
    response.status_code = status.HTTP_307_TEMPORARY_REDIRECT
    return RedirectResponse("/")


@router.get("/team", include_in_schema=True)
async def team(request: Request, response: Response):
    user = request.state.user
    if not os.path.exists("team.json"):
        await get_team_data()
    team_data = json.loads(open("team.json", "r").read())
    return templates.TemplateResponse(name="main/team.html", context={"request": request, "user": user, "team_data": team_data})
