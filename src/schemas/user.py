# 3rd party imports
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    age: int
    avatar: Optional[dict[str, int]] = {"body": 1, "face": 1, "eyes": 1, "mouth": 1, "hair": 1, "hat": 1}
    email: Optional[str] = None
    