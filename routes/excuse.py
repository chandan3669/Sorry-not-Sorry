from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from auth.auth_service import get_current_user
from auth.jwt_handler import verify_access_token
from database.db import get_db
from models.excuse_model import Excuse
from prompts.prompt_builder import build_excuse_prompt
from schemas.excuse_schema import ExcuseHistoryItem, ExcuseRequest, ExcuseResponse
from services.ai_service import AIServiceError, generate_excuses
from services.score_service import generate_scores


router = APIRouter()


@router.post("/generate", response_model=ExcuseResponse)
def create_excuse(
    request: ExcuseRequest,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(verify_access_token),
):
    try:
        current_user = get_current_user(token_payload, db)
        prompt = build_excuse_prompt(request)
        excuse_texts = generate_excuses(prompt)
        responses = []

        for index, excuse_text in enumerate(excuse_texts, start=1):
            scores = generate_scores()
            excuse = Excuse(
                user_id=current_user.id,
                category=request.category.strip(),
                audience=request.audience.strip(),
                tone=request.tone.strip(),
                length=request.length.strip(),
                excuse=excuse_text,
                believability=scores["believability"],
                drama=scores["drama"],
                risk=scores["risk"],
            )

            db.add(excuse)
            responses.append(
                {
                    "id": index,
                    "text": excuse_text,
                    "believability": scores["believability"],
                    "drama": scores["drama"],
                    "risk": scores["risk"],
                }
            )

        db.commit()

        return ExcuseResponse(responses=responses)
    except AIServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save generated excuse",
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while generating excuse",
        ) from exc


@router.get("/history", response_model=list[ExcuseHistoryItem])
def get_history(
    db: Session = Depends(get_db),
    token_payload: dict = Depends(verify_access_token),
):
    try:
        current_user = get_current_user(token_payload, db)
        return (
            db.query(Excuse)
            .filter(Excuse.user_id == current_user.id)
            .order_by(Excuse.created_at.desc())
            .all()
        )
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch excuse history",
        ) from exc


@router.delete("/history/{excuse_id}")
def delete_history_item(
    excuse_id: int,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(verify_access_token),
):
    try:
        current_user = get_current_user(token_payload, db)
        excuse = (
            db.query(Excuse)
            .filter(Excuse.id == excuse_id, Excuse.user_id == current_user.id)
            .first()
        )
        if excuse is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Excuse not found",
            )

        db.delete(excuse)
        db.commit()
        return {"message": "Excuse deleted successfully"}
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete excuse",
        ) from exc


@router.get("/health")
def health_check():
    return {"status": "ok"}
