from src.dependencies import *
from src.schemas.announcement import Announcement
from datetime import datetime, timedelta

router = APIRouter(
    prefix="",
    tags=["Main"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", include_in_schema=True)
async def Main(request: Request, response: Response):
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