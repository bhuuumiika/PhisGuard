import { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000";

export default function Quiz() {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/api/quiz/questions`)
      .then((res) => res.json())
      .then(setQuestions)
      .catch(() => setError("Could not load quiz questions. Is the backend running?"))
      .finally(() => setLoading(false));
  }, []);

  function selectAnswer(qId, optionIndex) {
    setAnswers((prev) => ({ ...prev, [qId]: optionIndex }));
  }

  async function submit() {
    setError("");
    try {
      const res = await fetch(`${API_BASE}/api/quiz/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answers }),
      });
      if (!res.ok) throw new Error("failed");
      const data = await res.json();
      setResult(data);
    } catch {
      setError("Could not submit the quiz. Is the backend running?");
    }
  }

  function retake() {
    setAnswers({});
    setResult(null);
  }

  if (loading) return <div className="text-slate-500 text-sm">Loading quiz…</div>;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-xl font-bold text-slate-800 mb-1">Phishing Awareness Quiz</h2>
      <p className="text-slate-500 text-sm mb-4">
        Test what you've learned with a short, scored quiz.
      </p>

      {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

      {!result &&
        questions.map((q) => (
          <div key={q.id} className="mb-5">
            <p className="font-semibold text-slate-800 mb-2">
              {q.id}. {q.question}
            </p>
            <div className="space-y-2">
              {q.options.map((opt, idx) => (
                <label
                  key={idx}
                  className={`block border rounded-lg px-3 py-2 text-sm cursor-pointer transition ${
                    answers[q.id] === idx
                      ? "border-purple-500 bg-purple-50"
                      : "border-slate-200 hover:bg-slate-50"
                  }`}
                >
                  <input
                    type="radio"
                    name={`q-${q.id}`}
                    className="mr-2"
                    checked={answers[q.id] === idx}
                    onChange={() => selectAnswer(q.id, idx)}
                  />
                  {opt}
                </label>
              ))}
            </div>
          </div>
        ))}

      {!result && (
        <button
          onClick={submit}
          disabled={Object.keys(answers).length < questions.length}
          className="bg-purple-700 hover:bg-purple-800 disabled:opacity-40 text-white font-semibold px-5 py-2 rounded-lg text-sm transition"
        >
          Submit Quiz
        </button>
      )}

      {result && (
        <div>
          <div className="bg-purple-50 border border-purple-200 rounded-xl p-4 mb-4 text-center">
            <p className="text-3xl font-bold text-purple-800">
              {result.score} / {result.total}
            </p>
            <p className="text-slate-500 text-sm">Your score</p>
          </div>
          <div className="space-y-3 mb-4">
            {result.results.map((r) => (
              <div
                key={r.id}
                className={`border rounded-lg p-3 text-sm ${
                  r.correct ? "border-emerald-300 bg-emerald-50" : "border-red-300 bg-red-50"
                }`}
              >
                <p className="font-semibold mb-1">
                  {r.correct ? "✓" : "✗"} {r.question}
                </p>
                <p className="text-slate-600">{r.explanation}</p>
              </div>
            ))}
          </div>
          <button
            onClick={retake}
            className="bg-slate-700 hover:bg-slate-800 text-white font-semibold px-5 py-2 rounded-lg text-sm transition"
          >
            Retake Quiz
          </button>
        </div>
      )}
    </div>
  );
}
