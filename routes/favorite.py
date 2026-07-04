from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from auth.auth_service import get_current_user
from auth.jwt_handler import verify_access_token
from database.db import get_db
from models.excuse_model import Excuse
from models.favorite_model import Favorite
from schemas.favorite_schema import (
    FavoriteCreateRequest,
    FavoriteListResponse,
    FavoriteMessageResponse,
    FavoriteResponse,
)


router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post("", response_model=FavoriteMessageResponse)
def add_favorite(
    request: FavoriteCreateRequest,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(verify_access_token),
):
    try:
        current_user = get_current_user(token_payload, db)
        excuse = (
            db.query(Excuse)
            .filter(Excuse.id == request.excuse_id, Excuse.user_id == current_user.id)
            .first()
        )
        if excuse is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Excuse not found",
            )

        existing_favorite = (
            db.query(Favorite)
            .filter(
                Favorite.user_id == current_user.id,
                Favorite.excuse_id == request.excuse_id,
            )
            .first()
        )
        if existing_favorite:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Excuse already in favorites",
            )

        favorite = Favorite(user_id=current_user.id, excuse_id=request.excuse_id)
        db.add(favorite)
        db.commit()
        return {"message": "Added to favorites"}
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add favorite",
        ) from exc


@router.get("", response_model=FavoriteListResponse)
def get_favorites(
    db: Session = Depends(get_db),
    token_payload: dict = Depends(verify_access_token),
):
    try:
        current_user = get_current_user(token_payload, db)
        rows = (
            db.query(Favorite, Excuse)
            .join(Excuse, Favorite.excuse_id == Excuse.id)
            .filter(Favorite.user_id == current_user.id)
            .order_by(Favorite.created_at.desc())
            .all()
        )

        favorites = [
            FavoriteResponse(
                id=favorite.id,
                excuse=excuse.excuse,
                category=excuse.category,
                tone=excuse.tone,
                created_at=favorite.created_at,
            )
            for favorite, excuse in rows
        ]
        return FavoriteListResponse(favorites=favorites)
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch favorites",
        ) from exc


@router.delete("/{favorite_id}", response_model=FavoriteMessageResponse)
def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(verify_access_token),
):
    try:
        current_user = get_current_user(token_payload, db)
        favorite = (
            db.query(Favorite)
            .filter(Favorite.id == favorite_id, Favorite.user_id == current_user.id)
            .first()
        )
        if favorite is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found",
            )

        db.delete(favorite)
        db.commit()
        return {"message": "Favorite removed"}
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove favorite",
        ) from exc
