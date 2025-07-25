from pydantic import BaseModel, EmailStr, Field

class AuthRegisterRequest(BaseModel):
    first_name: str = Field(..., example="Juan")
    last_name: str = Field(..., example="Pérez")
    username: str = Field(..., min_length=3, example="juanp")
    email: EmailStr = Field(..., example="juan@gmail.com")
    password: str = Field(..., min_length=8, example="P@ssw0rd123")
