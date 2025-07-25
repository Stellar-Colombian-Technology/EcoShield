from pydantic import BaseModel
from typing import Optional

class AuthResponse(BaseModel):
    username: Optional[str]
    message: str
    jwt: Optional[str]
    status: bool
