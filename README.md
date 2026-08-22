# PhishGuard

A cybersecurity awareness web application that helps users learn to identify
phishing websites through interactive, hands-on practice.

Built as a Cyber Security Final (Capstone) Project.

## Problem Statement

**Online Safety** — Users often fail to identify phishing websites, leading to
data theft and scams.

## Features

- **URL Heuristics Checker** — submit any URL and get a 0–100 phishing risk
  score with specific reasons (missing HTTPS, IP-address hosts, typosquatted
  brand names, suspicious TLDs, URL shorteners, urgency keywords, and more).
- **Phishing vs. Real Website Demonstrator** — side-by-side comparisons of
  genuine sites and simulated phishing look-alikes, explaining exactly what
  gives each fake site away.
- **Phishing Awareness Quiz** — a short, scored quiz that reinforces
  phishing-recognition concepts with explanations for every answer.
- **Backend API + Data Layer** — FastAPI + SQLAlchemy + SQLite, logging every
  URL check and quiz attempt.
- **Automated Tests** — a pytest suite covering the heuristics engine and the
  quiz scoring logic.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS |
| Backend | FastAPI, SQLAlchemy |
| Database | SQLite |
| Testing | pytest |

## Project Structure

```
phishguard/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app entrypoint
│   │   ├── database.py        # SQLAlchemy engine/session setup
│   │   ├── models.py          # ORM models (URLCheck, QuizAttempt)
│   │   ├── heuristics.py      # URL phishing heuristics engine
│   │   ├── quiz_data.py       # Quiz question bank + grading logic
│   │   └── routers/
│   │       ├── heuristics.py  # /api/heuristics/* endpoints
│   │       └── quiz.py        # /api/quiz/* endpoints
│   ├── tests/
│   │   ├── test_heuristics.py
│   │   └── test_quiz.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   └── components/
    │       ├── URLChecker.jsx
    │       ├── PhishVsReal.jsx
    │       └── Quiz.jsx
    └── package.json
```

## Running Locally

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be live at `http://localhost:8000`. Interactive docs at
`http://localhost:8000/docs`.

### Run the backend tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be live at `http://localhost:5173` (Vite dev server) and will
call the backend at `http://localhost:8000`.

## Future Scope

- Integrate a live threat-intelligence / blocklist API for real-time phishing
  URL detection rather than heuristic-only analysis.
- Add machine-learning-based phishing classification trained on real
  phishing datasets to improve detection accuracy.
- Build a companion mobile application so users can check suspicious links
  directly from their phones.
- Introduce browser extension support to flag suspicious sites as users
  browse in real time.
- Expand the quiz and awareness modules to cover related threats such as
  smishing (SMS phishing) and vishing (voice phishing).

## Author

Bhumika — B.Tech, CSVTU
