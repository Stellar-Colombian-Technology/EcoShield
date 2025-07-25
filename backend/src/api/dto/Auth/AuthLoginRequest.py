from pydantic import BaseModel

class AuthLoginRequest(BaseModel):
    username: str
    password: str
