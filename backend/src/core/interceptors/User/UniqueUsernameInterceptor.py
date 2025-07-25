from sqlalchemy.orm import Session
from fastapi import Depends
from core.exceptions.UsernameAlreadyExistsException import UsernameAlreadyExistsException
from infrastructure.model.User import User
from infrastructure.config.Db import get_db

async def validate_unique_username(username: str, db: Session = Depends(get_db)) -> None:
    exists = db.query(User).filter(User.username == username).first() is not None
    if exists:
        raise UsernameAlreadyExistsException(username=username)