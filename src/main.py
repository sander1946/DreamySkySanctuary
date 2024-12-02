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
app.mount('/upload', StaticFiles(directory=config.UPLOAD_DIR), name='upload')
templates = Jinja2Templates(directory=config.TEMPLATES_DIR)


app.include_router(main_route.router)
app.include_router(bot_route.router)
# app.include_router(auth_route.router)

@app.exception_handler(FileTypeException)
async def unicorn_exception_handler(request: Request, exc: FileTypeException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": exc.message,
            "file_name": exc.file_name,
            "file_type": exc.file_type,
            "allowed_types": exc.allowed_types,
        },
    )

@app.on_event("startup")
@repeat_every(seconds=60*60)  # check every hour for expired files
def remove_expired_files_task():
    remove_expired_files(path=config.UPLOAD_DIR, expire_time=config.UPLOAD_EXPIRE_TIME)
