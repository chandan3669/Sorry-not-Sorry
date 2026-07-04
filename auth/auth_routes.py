from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.auth_service import (
    get_current_user,
    login_user,
    logout_user,
    register_user,
    update_user_profile,
)
from auth.jwt_handler import verify_access_token
from database.db import get_db
from schemas.auth_schema import (
    LoginRequest,
    MessageResponse,
    ProfileUpdateRequest,
    RegisterRequest,
    TokenResponse,
    UserProfileResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MessageResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(request, db)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(request, db)


@router.post("/logout", response_model=MessageResponse)
def logout():
    return logout_user()


@router.get("/me", response_model=UserProfileResponse)
def me(
    token_payload: dict = Depends(verify_access_token),
    db: Session = Depends(get_db),
):
    return get_current_user(token_payload, db)


@router.put("/profile", response_model=MessageResponse)
def update_profile(
    request: ProfileUpdateRequest,
    token_payload: dict = Depends(verify_access_token),
    db: Session = Depends(get_db),
):
    return update_user_profile(request, token_payload, db)
