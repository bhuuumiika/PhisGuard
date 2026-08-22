import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.heuristics import analyze_url


def test_legit_https_domain_scores_low():
    result = analyze_url("https://www.google.com/search?q=test")
    assert result["risk_score"] < 30
    assert result["verdict"] == "likely safe"


def test_ip_address_url_is_flagged():
    result = analyze_url("http://192.168.1.10/login")
    assert result["risk_score"] >= 25
    assert any("IP address" in r for r in result["reasons"])


def test_missing_https_is_flagged():
    result = analyze_url("http://example.com/account")
    assert any("HTTPS" in r for r in result["reasons"])


def test_typosquat_brand_detected():
    result = analyze_url("http://paypa1.com/verify-account")
    assert result["risk_score"] >= 30
    assert result["verdict"] in ("suspicious", "likely phishing")


def test_at_symbol_detected():
    result = analyze_url("http://google.com@malicious-site.tk/login")
    assert any("@" in r for r in result["reasons"])
    assert result["risk_score"] >= 25


def test_url_shortener_flagged():
    result = analyze_url("https://bit.ly/3xample")
    assert any("shortening" in r for r in result["reasons"])


def test_empty_url_handled_gracefully():
    result = analyze_url("")
    assert result["verdict"] == "unknown"


def test_high_risk_combo_is_likely_phishing():
    result = analyze_url("http://secure-verify-paypa1-login.tk/confirm-account")
    assert result["verdict"] == "likely phishing"
    assert result["risk_score"] >= 60
