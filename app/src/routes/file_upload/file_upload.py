from src.dependencies import *
import hashlib
import shutil
from src.schemas.errors.FileNotFoundException import FileNotFoundException
from src.schemas.errors.FileTypeException import FileTypeException
from fastapi import status

router = APIRouter(
    prefix="",
    tags=["Upload"],
)

templates = Jinja2Templates(directory="templates")

@router.get("/upload", include_in_schema=True)
async def main(request: Request, response: Response):
    string_types = ""
    for type in config.ALLOWED_FILE_TYPES:
        string_types += f"{type}, "
    return templates.TemplateResponse(name="main/upload.html", context={"request": request, "allowed_types": string_types})


@router.post("/upload", include_in_schema=True)
async def upload_file(request: Request, uploaded_images: List[UploadFile] = File(...)):
    saved_files = []
    for image in uploaded_images:
        if image.content_type not in config.ALLOWED_FILE_TYPES:
            raise FileTypeException(image.filename, image.content_type, config.ALLOWED_FILE_TYPES)

        hash = hashlib.md5(str(image.filename).encode("utf-8"))
        filename = f"{hash.hexdigest()}.{config.ALLOWED_FILE_TYPES[image.content_type]}"
        filename = filename[-15:]
        save_path = os.path.join(config.UPLOAD_DIR, filename)
        
        with open(save_path, "wb+") as f:
            shutil.copyfileobj(image.file, f)
            print(f"File {image.filename} saved as {filename} in {config.UPLOAD_DIR}")
        image_data = {
            'filename': filename,
            'path': save_path,
            'url': f"/images/{filename}",
            'auth_code': hash.hexdigest()[:11]
        }
        saved_files.append(image_data)
        images[filename] = image_data
    
    if len(saved_files) == 1:
        print(f"Image {saved_files[0]['filename']} uploaded with manage code {saved_files[0]['auth_code']}")
        return RedirectResponse(f"/image/{saved_files[0]['filename']}/{saved_files[0]['auth_code']}", status_code=status.HTTP_303_SEE_OTHER)
    if len(saved_files) > 1:
        hashstring = ""
        for image in saved_files:
            hashstring += image['filename']
        gallery_hash = hashlib.md5(str(hashstring).encode("utf-8"))
        gallery_code = gallery_hash.hexdigest()[11:]
        auth_code = gallery_hash.hexdigest()[:11]
        print(f"Gallery {gallery_code} created with manage code {auth_code}")
        
        gallerys[gallery_code] = {
            "images": saved_files,
            "auth_code": auth_code
        }
        
        return RedirectResponse(f"/gallery/{gallery_code}/{auth_code}", status_code=status.HTTP_303_SEE_OTHER)
    
    return RedirectResponse("/upload", status_code=status.HTTP_400_BAD_REQUEST)


images: dict[str, dict[str, any]] = {
    "1d3313c274e.png": {
        'filename': "1d3313c274e.png",
        'path': os.path.join(config.UPLOAD_DIR, "1d3313c274e.png"),
        'url': "/images/1d3313c274e.png",
        'auth_code': "867df75944b"
    },
    "3da70602ac6.png": {
        'filename': "3da70602ac6.png",
        'path': os.path.join(config.UPLOAD_DIR, "3da70602ac6.png"),
        'url': "/images/3da70602ac6.png",
        'auth_code': "3da70602ac6"
    }
}

gallerys: dict[str:dict[str, any]] = {
    "test": {
        "images": [
            images["1d3313c274e.png"],
            images["3da70602ac6.png"]
        ],
        "auth_code": "test"
    }
}


@router.get('/gallery/{gallery_code}')
async def gallery(request: Request, gallery_code: str):
    # return JSONResponse({"gallery_code": gallery_code})
    
    if gallery_code not in gallerys:
        raise FileNotFoundException(file_name=gallery_code, message="Gallery not found.")
    
    images = gallerys[gallery_code]["images"]
    return templates.TemplateResponse(
        name="main/gallery.html",
        context={"request": request, "images": images}
    )


@router.get('/gallery/{gallery_code}/{auth_code}')
async def gallery(request: Request, gallery_code: str, auth_code: str):
    # return JSONResponse({"gallery_code": gallery_code, "auth_code": auth_code})
    
    if gallery_code not in gallerys:
        raise FileNotFoundException(file_name=gallery_code, message="Gallery not found.")
    
    images = gallerys[gallery_code]
    
    if auth_code != images["auth_code"]:
        return RedirectResponse(f"/gallery/{gallery_code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    
    return templates.TemplateResponse(
        name="main/gallery.html",
        context={"request": request, "images": images["images"], "auth_code": auth_code}
    )


@router.get('/image/{file_name}')
async def image(request: Request, file_name: str):
    # return JSONResponse({"file_name": file_name})
    
    if file_name not in images:
        raise FileNotFoundException(file_name=file_name, message="Image not found.")
    
    image = images[file_name]
    
    return templates.TemplateResponse(
        name="main/image.html",
        context={"request": request, "image": image}
    )


@router.get('/image/{file_name}/{auth_code}')
async def manage_image(request: Request, file_name: str, auth_code: str):
    # return JSONResponse({"file_name": file_name, "auth_code": auth_code})

    if file_name not in images:
        raise FileNotFoundException(file_name=file_name, message="Image not found.")
    
    image = images[file_name]
    
    if auth_code != image["auth_code"]:
        return RedirectResponse(f"/image/{file_name}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    
    return templates.TemplateResponse(
        name="main/image.html",
        context={"request": request, "image": image, "auth_code": auth_code}
    )


@router.get('/remove/{file_name}/{auth_code}')
async def remove_image(file_name: str, auth_code: str):
    if file_name not in images:
        raise FileNotFoundException(file_name=file_name, message="Image not found.")
    
    image = images[file_name]
    
    if auth_code != image["auth_code"]: 
        return RedirectResponse(f"/image/{file_name}", status_code=status.HTTP_401_UNAUTHORIZED)
    
    print(f"Image {file_name} removed from {image['path']}")
    os.remove(image["path"])
    images.pop(file_name)
    for gallery_key in gallerys.keys():
        for image in gallerys[gallery_key]["images"]:
            if image["filename"] == file_name:
                gallerys[gallery_key]["images"].remove(image)
    
    return RedirectResponse("/upload", status_code=status.HTTP_303_SEE_OTHER)


@router.get('/remove/{gallery_code}/{auth_code}')
async def remove_gallery(gallery_code: str, auth_code: str):
    if gallery_code not in gallerys:
        raise FileNotFoundException(file_name=gallery_code, message="Gallery not found.")
    
    gallery = gallerys[gallery_code]
    
    if auth_code != gallery["auth_code"]:
        return RedirectResponse(f"/gallery/{gallery_code}", status_code=status.HTTP_401_UNAUTHORIZED)
    
    for image in gallery["images"]:
        os.remove(image["path"])
        images.pop(image["filename"])
    
    gallerys.pop(gallery_code)
    
    return RedirectResponse("/upload", status_code=status.HTTP_303_SEE_OTHER)


@router.get('/i/{file_name}')
async def download(file_name: str):
    file_path = os.path.join(config.UPLOAD_DIR, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundException(file_name=file_name, file_path=file_path)
    return FileResponse(path=file_path, filename=file_name)