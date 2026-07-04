from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from database.db import Base


class Excuse(Base):
    __tablename__ = "excuses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    category = Column(String, nullable=False)
    audience = Column(String, nullable=False)
    tone = Column(String, nullable=False)
    length = Column(String, nullable=False)
    excuse = Column(Text, nullable=False)
    believability = Column(Integer, nullable=False)
    drama = Column(Integer, nullable=False)
    risk = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
