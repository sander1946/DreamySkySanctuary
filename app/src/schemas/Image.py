# 3rd party imports
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

class ImageData(BaseModel):
    filename: str = Field(..., min_length=15, max_length=15)
    auth_code: str = Field(..., min_length=15, max_length=15)
    path: str = Field(..., max_length=100)
    url: str = Field(..., max_length=100)
    filesize: int
    delete_after: Optional[datetime] = None
    uploaded_by: Optional[str] = Field(None, min_length=2, max_length=32)

class GalleryData(BaseModel):
    gallery_code: str = Field(..., min_length=15, max_length=15)
    auth_code: str = Field(..., min_length=15, max_length=15)
    delete_after: Optional[datetime] = None
    uploaded_by: Optional[str] = Field(None, min_length=2, max_length=32)
    preview_image: Optional[str] = Field(None, max_length=100)


class ImageGalleryLink(BaseModel):
    gallery_code: str = Field(..., min_length=15, max_length=15)
    filename: str = Field(..., max_length=100)