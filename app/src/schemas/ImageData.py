# 3rd party imports
from pydantic import BaseModel

class ImageData(BaseModel):
    filename: str
    auth_code: str
    path: str
    url: str
    filesize: int