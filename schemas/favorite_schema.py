from datetime import datetime

from pydantic import BaseModel, Field


class FavoriteCreateRequest(BaseModel):
    excuse_id: int = Field(..., gt=0)


class FavoriteResponse(BaseModel):
    id: int
    excuse: str
    category: str
    tone: str
    created_at: datetime


class FavoriteListResponse(BaseModel):
    favorites: list[FavoriteResponse]


class FavoriteMessageResponse(BaseModel):
    message: str
