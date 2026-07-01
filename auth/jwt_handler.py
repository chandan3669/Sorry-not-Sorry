import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt


load_dotenv()

security = HTTPBearer()


def _get_secret_key() -> str:
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SECRET_KEY not found",
        )
    return secret_key


def _get_algorithm() -> str:
    return os.getenv("ALGORITHM", "HS256")


def _get_access_token_expire_minutes() -> int:
    return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def create_access_token(data: dict) -> str:
    token_data = data.copy()
    expires_delta = timedelta(minutes=_get_access_token_expire_minutes())
    token_data.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(token_data, _get_secret_key(), algorithm=_get_algorithm())


def verify_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    try:
        return jwt.decode(
            credentials.credentials,
            _get_secret_key(),
            algorithms=[_get_algorithm()],
        )
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
