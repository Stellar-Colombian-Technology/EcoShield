from fastapi import HTTPException, Depends
from core.exceptions.HaveConfirmedEmailException import HaveConfirmedEmailException
from infrastructure.model.User import User  

async def validate_confirmed_email(user: User):
    if not user.is_verified:
        raise HaveConfirmedEmailException(email=user.email)