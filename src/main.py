from src.dependencies import *

# app config
app = FastAPI(
    title=config.APP_NAME,
    description=config.DESCRIPTION,
    version=config.VERSION,
)

# mount static files
app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")
app.mount("/public", StaticFiles(directory=config.PUBLIC_DIR), name="public")
templates = Jinja2Templates(directory=config.TEMPLATES_DIR)


app.include_router(main_route.router)
app.include_router(bot_route.router)
# app.include_router(auth_route.router)