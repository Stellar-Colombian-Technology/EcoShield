from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from infrastructure.config.Db import get_db
from core.service.AuthService import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    request_data = await request.json()
    return await auth_service.login(request_data, db)


@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    request_data = await request.json()
    return await auth_service.register(request_data, db)


@router.get("/verify-email")
async def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    return auth_service.verify_email(token, db)
