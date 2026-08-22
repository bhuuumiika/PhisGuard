import { useState } from "react";
import URLChecker from "./components/URLChecker";
import PhishVsReal from "./components/PhishVsReal";
import Quiz from "./components/Quiz";

const TABS = [
  { id: "checker", label: "URL Checker" },
  { id: "compare", label: "Phishing vs Real" },
  { id: "quiz", label: "Quiz" },
];

export default function App() {
  const [tab, setTab] = useState("checker");

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-gradient-to-r from-purple-800 to-purple-600 text-white">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-3xl">🛡️</span>
            <h1 className="text-3xl font-extrabold">PhishGuard</h1>
          </div>
          <p className="text-purple-100">
            Learn to spot phishing websites before they catch you — scan URLs, compare
            real vs. fake sites, and test your knowledge.
          </p>
        </div>
      </header>

      <nav className="max-w-4xl mx-auto px-6 -mt-5">
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-1.5 flex gap-1">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`flex-1 py-2 rounded-lg text-sm font-semibold transition ${
                tab === t.id
                  ? "bg-purple-700 text-white"
                  : "text-slate-500 hover:bg-slate-100"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-6 py-8">
        {tab === "checker" && <URLChecker />}
        {tab === "compare" && <PhishVsReal />}
        {tab === "quiz" && <Quiz />}
      </main>

      <footer className="text-center text-xs text-slate-400 pb-6">
        PhishGuard — Cyber Security Capstone Project
      </footer>
    </div>
  );
}
