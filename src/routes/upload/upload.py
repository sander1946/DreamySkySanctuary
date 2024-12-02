from src.dependencies import *

router = APIRouter(
    prefix="",
    tags=["Upload"],
)

templates = Jinja2Templates(directory="templates")

@router.get("/", include_in_schema=True)
async def main(request: Request, response: Response):
    return templates.TemplateResponse(name="upload/index.html", context={"request": request})
