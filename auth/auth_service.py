from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from auth.jwt_handler import create_access_token
from auth.password_handler import hash_password, verify_password
from models.user_model import User
from schemas.auth_schema import LoginRequest, RegisterRequest


def register_user(request: RegisterRequest, db: Session) -> dict[str, str]:
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
