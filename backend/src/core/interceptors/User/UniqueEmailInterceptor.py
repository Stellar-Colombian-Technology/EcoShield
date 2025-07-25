from sqlalchemy.orm import Session
from fastapi import Depends
from core.exceptions.EmailAlreadyExistsException import EmailAlreadyExistsException
from infrastructure.model.User import User
from infrastructure.config.Db import get_db  

async def validate_unique_email(email: str, db: Session = Depends(get_db)) -> None:
    exists = db.query(User).filter(User.email == email).first() is not None
    if exists:
        raise EmailAlreadyExistsException(email=email)