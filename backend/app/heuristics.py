"""
URL Heuristics Engine
---------------------
A lightweight, rule-based scorer that inspects a URL for common phishing
indicators. This is intentionally heuristic (no external threat-intel
lookups) so it works fully offline and is easy to explain/demo.

Each triggered rule contributes weighted points to a 0-100 risk score.
"""

import re
from urllib.parse import urlparse

# Brands frequently impersonated in phishing campaigns, used to detect
# look-alike / typosquatted domains (e.g. "paypa1.com", "amaz0n-secure.com").
COMMON_BRANDS = [
    "paypal", "amazon", "google", "microsoft", "apple", "facebook",
    "instagram", "netflix", "bankofamerica", "chase", "wellsfargo",
    "hdfcbank", "icicibank", "sbi", "whatsapp", "linkedin",
]

SUSPICIOUS_TLDS = {".zip", ".xyz", ".top", ".tk", ".gq", ".ml", ".cf", ".click", ".work"}
URL_SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly"}
URGENCY_WORDS = ["verify", "urgent", "suspended", "locked", "confirm", "update-account", "secure-login"]


def _levenshtein(a: str, b: str) -> int:
    """Standard edit distance, used for brand look-alike detection."""
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            curr[j] = min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost)
        prev = curr
    return prev[-1]


def analyze_url(raw_url: str) -> dict:
    """
    Analyze a URL and return a risk score (0-100), a verdict, and the
    specific reasons that contributed to the score.
    """
    reasons = []
    score = 0

    url = raw_url.strip()
    if not url:
        return {"url": raw_url, "risk_score": 0, "verdict": "unknown", "reasons": ["Empty URL submitted."]}

    if not re.match(r"^https?://", url, re.IGNORECASE):
        url_for_parse = "http://" + url
    else:
        url_for_parse = url

    parsed = urlparse(url_for_parse)
    host = (parsed.hostname or "").lower()
    scheme = parsed.scheme.lower()
    path_and_query = (parsed.path or "") + ("?" + parsed.query if parsed.query else "")

    # 1. Missing HTTPS
    if scheme != "https":
        score += 15
        reasons.append("Connection is not secured with HTTPS.")

    # 2. IP address used instead of a domain name
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        score += 25
        reasons.append("Uses a raw IP address instead of a domain name.")

    # 3. Excessive subdomains (e.g. secure-login.paypal.com.verify-user.xyz)
    if host.count(".") >= 4:
        score += 15
        reasons.append("Unusually large number of subdomains.")

    # 4. '@' symbol in URL (browsers ignore everything before '@' when resolving host)
    if "@" in url:
        score += 25
        reasons.append("Contains an '@' symbol, which can hide the real destination.")

    # 5. Suspicious / free TLDs
    if any(host.endswith(tld) for tld in SUSPICIOUS_TLDS):
        score += 15
        reasons.append("Uses a top-level domain commonly abused for phishing.")

    # 6. Known URL shorteners (hide the real destination)
    if host in URL_SHORTENERS:
        score += 15
        reasons.append("Uses a URL-shortening service, which conceals the real destination.")

    # 7. Hyphens in domain (often used to imitate real brands, e.g. paypal-secure.com)
    if host.count("-") >= 2:
        score += 10
        reasons.append("Domain contains multiple hyphens, a common look-alike tactic.")

    # 8. Brand look-alike / typosquat detection
    domain_labels = host.split(".")
    core_label = domain_labels[-2] if len(domain_labels) >= 2 else host
    # Also check each hyphen-separated segment (e.g. "secure-verify-paypa1-login")
    segments = {core_label, *core_label.split("-")}
    matched_brand = False
    for brand in COMMON_BRANDS:
        for segment in segments:
            if brand == segment:
                continue
            distance = _levenshtein(segment, brand)
            if 0 < distance <= 2 and len(segment) >= 4:
                score += 30
                reasons.append(f"Domain closely resembles the brand '{brand}' (possible typosquat).")
                matched_brand = True
                break
            if brand in host and brand != segment:
                score += 20
                reasons.append(f"Brand name '{brand}' appears outside the main domain label.")
                matched_brand = True
                break
        if matched_brand:
            break

    # 9. Urgency / credential-harvesting keywords in path or query
    lowered_path = path_and_query.lower()
    if any(word in lowered_path for word in URGENCY_WORDS):
        score += 10
        reasons.append("URL path contains urgency/verification keywords typical of phishing.")

    # 10. Very long URL (often used to obscure the real domain)
    if len(url) > 90:
        score += 10
        reasons.append("Unusually long URL, which can be used to bury the real domain.")

    score = min(score, 100)

    if score >= 60:
        verdict = "likely phishing"
    elif score >= 30:
        verdict = "suspicious"
    else:
        verdict = "likely safe"

    if not reasons:
        reasons.append("No common phishing indicators detected.")

    return {"url": raw_url, "risk_score": score, "verdict": verdict, "reasons": reasons}
