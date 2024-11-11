from src.dependencies import *
from src.schemas.announcement import Announcement
from datetime import datetime, timedelta

from src.routes.bot.bot import fetch_by_id

router = APIRouter(
    prefix="",
    tags=["Main"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", include_in_schema=True)
async def main(request: Request, response: Response):
    response.status_code = status.HTTP_200_OK
    announcements = [
        Announcement(title="Welcome to the API",
        description = "This is a simple API that uses FastAPI and Jinja2 to render HTML templates.",
        author = "Kai",
        date = datetime.now()),
        Announcement(title="This is a test announcement",
        description = "This is a test announcement to show how the announcements are displayed.",
        date = datetime.now() - timedelta(days=1),
        image = "/public/imgs/flags/en.png"),
    ]
    return templates.TemplateResponse(name="main/index.html", context={"request": request, "announcements": announcements})


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
    response.status_code = status.HTTP_200_OK
    owner_id = [529007366365249546]
    owner_data = []
    celestial_id = [485157849211863040]
    celestial_data = []
    guardian_id = [435848199551451146, 640935141958483978, 187126200873910272]
    guardian_data = []
    tech_id = [371350209160019970]
    tech_data = []
    lumi_id = [736117868864733234, 1055723680979746896, 628517615270363137, 1218643132363702352, 971730515256287303, 713397233936105532]
    lumi_data = []
    for _id in owner_id:
        return_data, _ = await fetch_by_id(_id)
        owner_data.append(return_data["user"])
        owner_info = "The founder of the community!"
    for _id in celestial_id:
        return_data, _ = await fetch_by_id(_id)
        celestial_data.append(return_data["user"])
        celestial_info = "Administrator of the community!"
    for _id in guardian_id:
        return_data, _ = await fetch_by_id(_id)
        guardian_data.append(return_data["user"])
        guardian_info = "The community moderators!"
    for _id in tech_id:
        return_data, _ = await fetch_by_id(_id)
        tech_data.append(return_data["user"])
        tech_info = "The one who manages the bot!"
    for _id in lumi_id:
        return_data, _ = await fetch_by_id(_id)
        lumi_data.append(return_data["user"])
        lumi_info = "The community event holders!"
    team_data = {"Sanctuary Keeper": (owner_data, owner_info), "celestial": (celestial_data, celestial_info), "guardian": (guardian_data, guardian_info), "tech": (tech_data, tech_info), "lumi": (lumi_data, lumi_info)}
    return templates.TemplateResponse(name="main/team.html", context={"request": request, "team_data": team_data})
