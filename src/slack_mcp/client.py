from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv
from slack_sdk.web.async_client import AsyncWebClient

load_dotenv()

_SLACK_BASE_URL = "https://slack.com/api/"


class SlackClient:
    """Unified Slack API client using xoxp for official methods
    and xoxc + xoxd for undocumented session endpoints."""

    def __init__(self) -> None:
        self.xoxp_token = os.environ.get("SLACK_XOXP_TOKEN", "")
        self.xoxc_token = os.environ.get("SLACK_XOXC_TOKEN", "")
        self.xoxd_token = os.environ.get("SLACK_XOXD_TOKEN", "")

        self.web_client = AsyncWebClient(token=self.xoxp_token)

        self.session_client = httpx.AsyncClient(
            base_url=_SLACK_BASE_URL,
            headers={"Authorization": f"Bearer {self.xoxc_token}"},
            cookies={"d": self.xoxd_token},
        )

    async def api_call(self, method: str, **kwargs) -> dict:
        """Call an official Slack Web API method via slack_sdk (form-encoded)."""
        response = await self.web_client.api_call(method, data=kwargs)
        return dict(response.data)

    async def api_call_json(self, method: str, **kwargs) -> dict:
        """Call an official Slack Web API method via slack_sdk (JSON body).

        Some methods (e.g. files.completeUploadExternal) require complex
        nested objects that must be sent as JSON rather than form-encoded.
        """
        response = await self.web_client.api_call(method, json=kwargs)
        return dict(response.data)

    def _require_session_tokens(self) -> None:
        if not self.xoxc_token or not self.xoxd_token:
            raise ValueError(
                "Session tokens (SLACK_XOXC_TOKEN and SLACK_XOXD_TOKEN) are required "
                "for undocumented endpoints. Grab them from your browser cookies while "
                "logged into slack.com."
            )

    def _check_session_response(self, data: dict, method: str) -> dict:
        if not data.get("ok"):
            error = data.get("error", "unknown_error")
            if error in (
                "not_authed",
                "invalid_auth",
                "token_expired",
                "token_revoked",
            ):
                raise ValueError(
                    f"Session endpoint {method} failed: {error}. "
                    "Your xoxc/xoxd tokens may be expired — re-grab them "
                    "from browser cookies while logged into slack.com."
                )
        return data

    async def session_call(self, method: str, **kwargs) -> dict:
        """Call an undocumented Slack endpoint using xoxc + xoxd auth."""
        self._require_session_tokens()
        resp = await self.session_client.post(method, json=kwargs)
        resp.raise_for_status()
        return self._check_session_response(resp.json(), method)

    async def session_call_form(self, method: str, **kwargs) -> dict:
        """Call an undocumented Slack endpoint with form-encoded data.

        Some legacy endpoints (e.g. files.edit) require form-encoded data
        rather than JSON.
        """
        self._require_session_tokens()
        resp = await self.session_client.post(
            method,
            data=kwargs,
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
            },
        )
        resp.raise_for_status()
        return self._check_session_response(resp.json(), method)

    async def session_call_multipart(
        self, method: str, data: dict, files: dict
    ) -> dict:
        """Call an undocumented Slack endpoint with multipart form data."""
        self._require_session_tokens()
        resp = await self.session_client.post(method, data=data, files=files)
        resp.raise_for_status()
        return self._check_session_response(resp.json(), method)

    async def close(self) -> None:
        await self.session_client.aclose()


_client: SlackClient | None = None


def get_client() -> SlackClient:
    """Return a module-level singleton SlackClient instance."""
    global _client
    if _client is None:
        _client = SlackClient()
    return _client
