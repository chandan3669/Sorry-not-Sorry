from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from auth.jwt_handler import create_access_token
from auth.password_handler import hash_password, verify_password
from models.user_model import User
from schemas.auth_schema import LoginRequest, ProfileUpdateRequest, RegisterRequest

def register_user(request: RegisterRequest, db: Session) -> dict[str, str]:
    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    try:
        user = User(
            username=request.username.strip(),
            email=request.email.lower(),
            hashed_password=hash_password(request.password),
        )
        db.add(user)
        db.commit()
        return {"message": "User registered successfully"}
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user",
        ) from exc


def login_user(request: LoginRequest, db: Session) -> dict[str, str]:
    user = db.query(User).filter(User.email == request.email.lower()).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}


def logout_user() -> dict[str, str]:
    return {"message": "Logged out successfully"}


def get_current_user(token_payload: dict, db: Session) -> User:
    user_id = token_payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def update_user_profile(
    request: ProfileUpdateRequest,
    token_payload: dict,
    db: Session,
) -> dict[str, str]:
    user = get_current_user(token_payload, db)

    if request.email is not None:
        new_email = request.email.lower()
        existing_user = db.query(User).filter(User.email == new_email).first()
        if existing_user and existing_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        user.email = new_email

    if request.username is not None:
        user.username = request.username.strip()

    try:
        db.commit()
        return {"message": "Profile updated successfully"}
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile",
        ) from exc
