from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import heuristics, quiz

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PhishGuard API",
    description="Cybersecurity awareness API: URL heuristics engine and phishing-awareness quiz.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(heuristics.router)
app.include_router(quiz.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "PhishGuard API"}
