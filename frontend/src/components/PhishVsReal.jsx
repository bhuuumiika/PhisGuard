import { useState } from "react";

const PAIRS = [
  {
    brand: "PayPal",
    real: {
      label: "Genuine site",
      url: "https://www.paypal.com/signin",
      notes: [
        "Domain is exactly paypal.com — no extra words or characters",
        "Uses HTTPS with a valid padlock",
        "No urgency language in the URL",
      ],
    },
    fake: {
      label: "Phishing site",
      url: "http://paypa1-secure-login.tk/verify-account",
      notes: [
        "'l' replaced with the digit '1' (typosquat)",
        "No HTTPS — plain http://",
        "Suspicious .tk domain and 'verify-account' urgency wording",
      ],
    },
  },
  {
    brand: "Bank Login",
    real: {
      label: "Genuine site",
      url: "https://www.icicibank.com/login",
      notes: [
        "Official bank domain, HTTPS enabled",
        "No hyphens or extra subdomains",
        "Straightforward /login path",
      ],
    },
    fake: {
      label: "Phishing site",
      url: "http://icicibank-secure-verify.xyz/confirm-account",
      notes: [
        "Extra words appended to the brand name after a hyphen",
        "Uses a free/suspicious .xyz TLD",
        "'confirm-account' urgency wording in the path",
      ],
    },
  },
  {
    brand: "Email Provider",
    real: {
      label: "Genuine site",
      url: "https://accounts.google.com",
      notes: [
        "Well-known, short, trusted subdomain of google.com",
        "HTTPS enabled",
        "No suspicious keywords",
      ],
    },
    fake: {
      label: "Phishing site",
      url: "http://accounts.google.com.security-check.click/login",
      notes: [
        "Real domain is pushed into the subdomain — actual domain is 'security-check.click'",
        "Suspicious .click TLD",
        "No HTTPS",
      ],
    },
  },
];

export default function PhishVsReal() {
  const [active, setActive] = useState(0);
  const pair = PAIRS[active];

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-xl font-bold text-slate-800 mb-1">Phishing vs. Real Website</h2>
      <p className="text-slate-500 text-sm mb-4">
        Compare a genuine site with a simulated phishing look-alike, and learn what gives it away.
      </p>

      <div className="flex flex-wrap gap-2 mb-5">
        {PAIRS.map((p, i) => (
          <button
            key={p.brand}
            onClick={() => setActive(i)}
            className={`text-sm px-3 py-1.5 rounded-full font-medium transition ${
              i === active
                ? "bg-purple-700 text-white"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            {p.brand}
          </button>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="border-2 border-emerald-300 bg-emerald-50 rounded-xl p-4">
          <span className="inline-block text-xs font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full mb-2">
            ✓ {pair.real.label}
          </span>
          <p className="font-mono text-sm break-all text-slate-700 mb-3">{pair.real.url}</p>
          <ul className="text-sm text-emerald-800 space-y-1 list-disc list-inside">
            {pair.real.notes.map((n, i) => (
              <li key={i}>{n}</li>
            ))}
          </ul>
        </div>

        <div className="border-2 border-red-300 bg-red-50 rounded-xl p-4">
          <span className="inline-block text-xs font-bold text-red-700 bg-red-100 px-2 py-0.5 rounded-full mb-2">
            ✗ {pair.fake.label}
          </span>
          <p className="font-mono text-sm break-all text-slate-700 mb-3">{pair.fake.url}</p>
          <ul className="text-sm text-red-800 space-y-1 list-disc list-inside">
            {pair.fake.notes.map((n, i) => (
              <li key={i}>{n}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
