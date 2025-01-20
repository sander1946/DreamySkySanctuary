from src.dependencies import *
import hashlib
import shutil
from src.schemas.FileNotFoundException import FileNotFoundException
from src.schemas.FileTypeException import FileTypeException

router = APIRouter(
    prefix="/up",
    tags=["Upload"],
)

templates = Jinja2Templates(directory="templates")

@router.get("/", include_in_schema=True)
async def main(request: Request, response: Response):
    string_types = ""
    for type in config.ALLOWED_FILE_TYPES:
        string_types += f"{type}, "
    return templates.TemplateResponse(name="main/upload.html", context={"request": request, "allowed_types": string_types})


@router.post("/", include_in_schema=True)
async def upload_file(request: Request, images: List[UploadFile] = File(...)):
    string_types = ", ".join(config.ALLOWED_FILE_TYPES)
    
    saved_files = []
    for image in images:
        if image.content_type not in config.ALLOWED_FILE_TYPES:
            raise FileTypeException(image.filename, image.content_type, config.ALLOWED_FILE_TYPES)    

        hash = hashlib.md5(str(image.filename).encode("utf-8"))
        filename = f"{hash.hexdigest()}.{config.ALLOWED_FILE_TYPES[image.content_type]}"
        filename = filename[-15:]
        save_path = os.path.join(config.UPLOAD_DIR, filename)
        
        with open(save_path, "wb+") as f:
            shutil.copyfileobj(image.file, f)
            print(f"File {image.filename} saved as {filename} in {config.UPLOAD_DIR}")
        saved_files.append({
            'original_filename': image.filename,
            'saved_filename': filename,
            'content_type': image.content_type,
            'path': save_path,
            'image_url': f"/images/{filename}",
        })
        
    return templates.TemplateResponse(
        name="main/upload.html", 
        context={
            "request": request,
            "files": saved_files,
            "allowed_types": string_types
        }
    )

@router.get('/download/{file_name}')
async def download(file_name: str):
    file_path = os.path.join(config.UPLOAD_DIR, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundException(file_name=file_name, file_path=file_path)
    return FileResponse(path=file_path, filename=file_name)