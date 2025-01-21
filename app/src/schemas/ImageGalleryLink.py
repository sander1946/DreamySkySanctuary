# 3rd party imports
from pydantic import BaseModel

class ImageGalleryLink(BaseModel):
    gallery_code: str
    filename: str