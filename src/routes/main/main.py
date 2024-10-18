from src.dependencies import *

router = APIRouter(
    prefix="",
    tags=["Main"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", include_in_schema=True)
async def Main(request: Request, response: Response):
    response.status_code = status.HTTP_200_OK
    return templates.TemplateResponse(name="main/index.html", context={"request": request})