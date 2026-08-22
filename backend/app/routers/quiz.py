from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict

from .. import models
from ..database import get_db
from ..quiz_data import get_quiz_questions, grade_quiz

router = APIRouter(prefix="/api/quiz", tags=["quiz"])


class QuizSubmission(BaseModel):
    answers: Dict[str, int]


@router.get("/questions")
def list_questions():
    return get_quiz_questions(include_answers=False)


@router.post("/submit")
def submit_quiz(payload: QuizSubmission, db: Session = Depends(get_db)):
    result = grade_quiz(payload.answers)

    attempt = models.QuizAttempt(score=result["score"], total=result["total"])
    db.add(attempt)
    db.commit()

    return result


@router.get("/leaderboard")
def leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    records = (
        db.query(models.QuizAttempt)
        .order_by(models.QuizAttempt.score.desc(), models.QuizAttempt.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {"id": r.id, "score": r.score, "total": r.total, "created_at": r.created_at}
        for r in records
    ]
