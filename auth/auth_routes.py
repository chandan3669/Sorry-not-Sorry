from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.auth_service import login_user, register_user
from database.db import get_db
from schemas.auth_schema import (
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    TokenResponse,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MessageResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(request, db)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(request, db)
