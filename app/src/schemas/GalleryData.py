# 3rd party imports
from pydantic import BaseModel

class GalleryData(BaseModel):
    gallery_code: str
    auth_code: str