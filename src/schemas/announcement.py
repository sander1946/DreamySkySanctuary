# 3rd party imports
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Announcement(BaseModel):
    title: str
    description: str
    author: Optional[str] = None
    date: datetime
    image: Optional[str] = None
    