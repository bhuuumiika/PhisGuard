import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..heuristics import analyze_url

router = APIRouter(prefix="/api/heuristics", tags=["heuristics"])


class URLCheckRequest(BaseModel):
    url: str


@router.post("/check")
def check_url(payload: URLCheckRequest, db: Session = Depends(get_db)):
    result = analyze_url(payload.url)

    record = models.URLCheck(
        url=result["url"],
        risk_score=result["risk_score"],
        verdict=result["verdict"],
        reasons=json.dumps(result["reasons"]),
    )
    db.add(record)
    db.commit()

    return result


@router.get("/history")
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    records = (
        db.query(models.URLCheck)
        .order_by(models.URLCheck.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": r.id,
            "url": r.url,
            "risk_score": r.risk_score,
            "verdict": r.verdict,
            "reasons": json.loads(r.reasons),
            "created_at": r.created_at,
        }
        for r in records
    ]
