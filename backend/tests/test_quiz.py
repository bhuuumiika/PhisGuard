import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.quiz_data import get_quiz_questions, grade_quiz, QUESTIONS


def test_questions_hide_answers_by_default():
    questions = get_quiz_questions()
    for q in questions:
        assert "answer_index" not in q
        assert "explanation" not in q


def test_questions_include_answers_when_requested():
    questions = get_quiz_questions(include_answers=True)
    for q in questions:
        assert "answer_index" in q


def test_perfect_score():
    answers = {str(q["id"]): q["answer_index"] for q in QUESTIONS}
    result = grade_quiz(answers)
    assert result["score"] == result["total"] == len(QUESTIONS)


def test_zero_score():
    # pick a deliberately wrong option for every question
    answers = {
        str(q["id"]): (q["answer_index"] + 1) % len(q["options"])
        for q in QUESTIONS
    }
    result = grade_quiz(answers)
    assert result["score"] == 0


def test_partial_score_and_result_shape():
    answers = {str(QUESTIONS[0]["id"]): QUESTIONS[0]["answer_index"]}
    result = grade_quiz(answers)
    assert result["score"] == 1
    assert result["total"] == len(QUESTIONS)
    assert len(result["results"]) == len(QUESTIONS)
    assert result["results"][0]["correct"] is True
