# 3rd party imports
from pydantic import BaseModel, Field

class ImageData(BaseModel):
    filename: str = Field(..., min_length=15, max_length=15)
    auth_code: str = Field(..., min_length=15, max_length=15)
    path: str = Field(..., max_length=100)
    url: str = Field(..., max_length=100)
    filesize: int
    uploaded_by: str = Field(..., min_length=2, max_length=32)

class GalleryData(BaseModel):
    gallery_code: str = Field(..., min_length=15, max_length=15)
    auth_code: str = Field(..., min_length=15, max_length=15)


class ImageGalleryLink(BaseModel):
    gallery_code: str = Field(..., min_length=15, max_length=15)
    filename: str = Field(..., max_length=100)