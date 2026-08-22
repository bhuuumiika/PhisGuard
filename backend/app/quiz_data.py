"""Static quiz question bank and scoring helper for the awareness module."""

QUESTIONS = [
    {
        "id": 1,
        "question": "Which of these URLs is most likely a phishing attempt?",
        "options": [
            "https://www.paypal.com/signin",
            "http://paypa1-secure-login.xyz/verify-account",
            "https://accounts.google.com",
        ],
        "answer_index": 1,
        "explanation": "It swaps the letter 'l' for the digit '1', uses HTTP instead of HTTPS, a suspicious .xyz TLD, and urgency wording ('verify-account').",
    },
    {
        "id": 2,
        "question": "An email says your account will be 'permanently locked in 24 hours' unless you click a link. This is a red flag because:",
        "options": [
            "Legitimate companies never send account notices",
            "Urgency and fear are classic pressure tactics used in phishing",
            "24 hours is too short for any real deadline",
        ],
        "answer_index": 1,
        "explanation": "Phishing emails commonly create artificial urgency to make victims act before thinking carefully.",
    },
    {
        "id": 3,
        "question": "You hover over a link and the status bar shows a completely different domain than the link text. What should you do?",
        "options": [
            "Click it — the display text is what matters",
            "Do not click; the mismatched destination is a phishing indicator",
            "Only worry if the domain has no HTTPS",
        ],
        "answer_index": 1,
        "explanation": "A mismatch between displayed text and the actual destination URL is one of the most reliable phishing signals.",
    },
    {
        "id": 4,
        "question": "Which detail on a website is the strongest single indicator of legitimacy on its own?",
        "options": [
            "It has HTTPS enabled",
            "It looks visually identical to the real site",
            "No single detail alone guarantees legitimacy",
        ],
        "answer_index": 2,
        "explanation": "HTTPS and visual similarity can both be faked; real safety comes from checking several signals together (domain, HTTPS, sender, urgency, etc.).",
    },
    {
        "id": 5,
        "question": "A link uses a URL shortener (e.g., bit.ly) in an unsolicited message. This is:",
        "options": [
            "Always safe — shorteners are just for convenience",
            "A potential red flag, since it hides the real destination domain",
            "Only risky on social media, not email",
        ],
        "answer_index": 1,
        "explanation": "Shorteners are legitimate tools, but attackers frequently use them to hide malicious destinations behind a trusted-looking short link.",
    },
]


def get_quiz_questions(include_answers: bool = False):
    """Return quiz questions, optionally stripped of answers/explanations for the client."""
    if include_answers:
        return QUESTIONS
    return [
        {"id": q["id"], "question": q["question"], "options": q["options"]}
        for q in QUESTIONS
    ]


def grade_quiz(answers: dict) -> dict:
    """
    Grade a quiz submission.
    `answers` maps question id (int) -> selected option index (int).
    """
    total = len(QUESTIONS)
    score = 0
    results = []
    for q in QUESTIONS:
        selected = answers.get(str(q["id"]), answers.get(q["id"]))
        is_correct = selected == q["answer_index"]
        if is_correct:
            score += 1
        results.append({
            "id": q["id"],
            "question": q["question"],
            "correct": is_correct,
            "correct_index": q["answer_index"],
            "selected_index": selected,
            "explanation": q["explanation"],
        })
    return {"score": score, "total": total, "results": results}
