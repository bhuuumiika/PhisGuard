from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func

from .database import Base


class URLCheck(Base):
    """A logged record of a URL submitted to the heuristics engine."""

    __tablename__ = "url_checks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    risk_score = Column(Float, nullable=False)
    verdict = Column(String, nullable=False)
    reasons = Column(Text, nullable=False)  # JSON-encoded list of strings
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class QuizAttempt(Base):
    """A logged record of a completed quiz attempt."""

    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
