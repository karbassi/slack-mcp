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
        """Call an official Slack Web API method via slack_sdk."""
        response = await self.web_client.api_call(method, json=kwargs)
        return dict(response.data)

    async def session_call(self, method: str, **kwargs) -> dict:
        """Call an undocumented Slack endpoint using xoxc + xoxd auth."""
        resp = await self.session_client.post(method, json=kwargs)
        resp.raise_for_status()
        return resp.json()

    async def close(self) -> None:
        await self.session_client.aclose()


_client: SlackClient | None = None


def get_client() -> SlackClient:
    """Return a module-level singleton SlackClient instance."""
    global _client
    if _client is None:
        _client = SlackClient()
    return _client
