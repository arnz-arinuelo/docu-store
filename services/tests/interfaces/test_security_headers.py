"""Baseline security headers reach every response; the docs pages keep an open CSP."""

from fastapi.testclient import TestClient

from interfaces.api.main import app


def test_health_carries_baseline_headers() -> None:
    headers = TestClient(app).get("/health").headers
    assert headers["x-content-type-options"] == "nosniff"
    assert headers["x-frame-options"] == "DENY"
    assert headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert headers["permissions-policy"] == "camera=(), microphone=(), geolocation=()"
    assert headers["content-security-policy"] == "default-src 'none'; frame-ancestors 'none'"


def test_docs_page_has_no_csp() -> None:
    headers = TestClient(app).get("/docs").headers
    assert headers["x-frame-options"] == "DENY"
    assert "content-security-policy" not in headers
