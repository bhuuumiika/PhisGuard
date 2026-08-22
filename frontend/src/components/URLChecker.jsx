import { useState } from "react";

const API_BASE = "http://localhost:8000";

const VERDICT_STYLES = {
  "likely safe": "bg-emerald-50 border-emerald-300 text-emerald-800",
  "suspicious": "bg-amber-50 border-amber-300 text-amber-800",
  "likely phishing": "bg-red-50 border-red-300 text-red-800",
  "unknown": "bg-slate-50 border-slate-300 text-slate-700",
};

const EXAMPLES = [
  "https://www.google.com",
  "http://paypa1-secure-login.tk/verify-account",
  "http://192.168.10.5/wp-login",
];

export default function URLChecker() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleCheck(e) {
    e?.preventDefault();
    if (!url.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/api/heuristics/check`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      if (!res.ok) throw new Error("Request failed");
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Could not reach the PhishGuard API. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-xl font-bold text-slate-800 mb-1">URL Heuristics Checker</h2>
      <p className="text-slate-500 text-sm mb-4">
        Paste a URL below to scan it for common phishing indicators.
      </p>

      <form onSubmit={handleCheck} className="flex gap-2 mb-3">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="e.g. http://paypa1-secure-login.tk/verify-account"
          className="flex-1 border border-slate-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-purple-700 hover:bg-purple-800 disabled:opacity-50 text-white font-semibold px-5 py-2 rounded-lg text-sm transition"
        >
          {loading ? "Scanning..." : "Scan"}
        </button>
      </form>

      <div className="flex flex-wrap gap-2 mb-4">
        {EXAMPLES.map((ex) => (
          <button
            key={ex}
            onClick={() => setUrl(ex)}
            className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-600 px-2.5 py-1 rounded-full transition"
          >
            {ex}
          </button>
        ))}
      </div>

      {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

      {result && (
        <div className={`border rounded-xl p-4 ${VERDICT_STYLES[result.verdict] || VERDICT_STYLES.unknown}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="font-bold uppercase tracking-wide text-sm">{result.verdict}</span>
            <span className="font-mono text-sm">Risk score: {result.risk_score}/100</span>
          </div>
          <div className="w-full bg-white/60 rounded-full h-2 mb-3">
            <div
              className="h-2 rounded-full bg-current"
              style={{ width: `${result.risk_score}%` }}
            />
          </div>
          <ul className="list-disc list-inside text-sm space-y-1">
            {result.reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
