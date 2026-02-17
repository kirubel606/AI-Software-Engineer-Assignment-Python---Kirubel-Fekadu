import time

import requests
from datetime import datetime, timezone

from app.http_client import Client
from app.tokens import OAuth2Token, token_from_iso


def test_client_uses_requests_session():
    c = Client()
    assert isinstance(c.session, requests.Session)


def test_token_from_iso_uses_dateutil():
    t = token_from_iso("ok", "2099-01-01T00:00:00Z")
    assert isinstance(t, OAuth2Token)
    assert t.access_token == "ok"
    assert not t.expired


def test_api_request_sets_auth_header_when_token_is_valid():
    c = Client()
    c.oauth2_token = OAuth2Token(access_token="ok", expires_at=int(time.time()) + 3600)

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer ok"


def test_api_request_refreshes_when_token_is_missing():
    c = Client()
    c.oauth2_token = None

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer fresh-token"


def test_api_request_refreshes_when_token_is_dict():
    c = Client()
    c.oauth2_token = {"access_token": "stale", "expires_at": 0}

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer fresh-token"


def test_dict_token_missing_expires_at():
    c = Client()
    c.oauth2_token = {"access_token": "stale"}
    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer fresh-token"


def test_dict_token_not_expired():
    future_ts = int(datetime.now(tz=timezone.utc).timestamp()) + 3600
    c = Client()
    c.oauth2_token = {"access_token": "valid-dict", "expires_at": future_ts}

    resp = c.request("GET", "/me", api=True)
    
    assert resp["headers"].get("Authorization") is None


def test_expiring_oauth2token_refresh():
    ts_now = int(datetime.now(tz=timezone.utc).timestamp())
    c = Client()
    c.oauth2_token = OAuth2Token(access_token="old-token", expires_at=ts_now)

    resp = c.request("GET", "/me", api=True)
    assert resp["headers"].get("Authorization") == "Bearer fresh-token"


def test_custom_headers_preserved():
    c = Client()
    c.oauth2_token = None
    resp = c.request("GET", "/me", api=True, headers={"X-Test": "yes"})
    assert resp["headers"]["X-Test"] == "yes"
    assert resp["headers"]["Authorization"] == "Bearer fresh-token"


def test_non_api_request_ignores_token():
    c = Client()
    c.oauth2_token = None
    resp = c.request("GET", "/status", api=False)
    assert "Authorization" not in resp["headers"]
