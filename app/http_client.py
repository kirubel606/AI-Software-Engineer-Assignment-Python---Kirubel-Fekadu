from __future__ import annotations

from typing import Any, Dict, Optional, Union

import requests
from datetime import datetime, timezone

from .tokens import OAuth2Token


class Client:
    def __init__(self) -> None:
        self.oauth2_token: Union[OAuth2Token, Dict[str, Any], None] = None
        self.session = requests.Session()

    def refresh_oauth2(self) -> None:
        self.oauth2_token = OAuth2Token(access_token="fresh-token", expires_at=10**10)

    def request(
        self,
        method: str,
        path: str,
        *,
        api: bool = False,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        if headers is None:
            headers = {}

        # We make sure that both OAuth2Token and dict tokens are refreshed if they are expired not only just by checking of its a dictionary but alos checking if it expires at is less than the current time hence why i made a check for both and made datetime imports.
        if api:
            if not self.oauth2_token or (isinstance(self.oauth2_token, OAuth2Token) and self.oauth2_token.expired) or (isinstance(self.oauth2_token, dict) and self.oauth2_token.get("expires_at", 0) <= int(datetime.now(tz=timezone.utc).timestamp())):
                self.refresh_oauth2()

            if isinstance(self.oauth2_token, OAuth2Token):
                headers["Authorization"] = self.oauth2_token.as_header()

        req = requests.Request(method=method, url=f"https://example.com{path}", headers=headers)
        prepared = self.session.prepare_request(req)

        return {
            "method": method,
            "path": path,
            "headers": dict(prepared.headers),
        }