# 3rd party imports
from typing import Optional
from pydantic import BaseModel


class UpdateUser(BaseModel):
    username: Optional[str] = None
    age: Optional[int] = None
    avatar: Optional[dict[str, int]] = None
    email: Optional[str] = None
