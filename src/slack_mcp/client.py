from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv
from slack_sdk.web.async_client import AsyncWebClient

from slack_mcp.errors import is_auth_failure

# The MCP host owns which workspace the server talks to, injecting creds into the
# process env (${SLACK_XOXP_TOKEN} in .mcp.json), so the environment must win over
# a stray local .env. Test-workspace pinning lives in the test layer instead
# (conftest.py + the live_client team guard), not in a runtime override.
load_dotenv(override=False)

_SLACK_BASE_URL = "https://slack.com/api/"


def _drop_none(kwargs: dict) -> dict:
    """Drop keys whose value is None.

    Tools pass every Slack parameter through by keyword, leaving absent
    optionals as None. Slack's API has no "set to null" semantic — an omitted
    parameter and an explicit null are equivalent — so dropping None here lets
    tools forward arguments unconditionally without per-call ``if x is not None``
    guards. Falsy-but-meaningful values (False, 0, "", []) are preserved.
    """
    return {k: v for k, v in kwargs.items() if v is not None}


def _require_dict(data: object, method: str) -> dict:
    """Enforce that a Slack response payload is a ``dict``.

    ``SlackResponse.data`` is typed as ``dict | bytes`` — bytes appear when a
    method streams a raw file body. Every method routed through ``api_call`` /
    ``api_call_json`` returns JSON, so a non-dict payload is a contract
    violation; raise a clear error naming the method instead of letting a
    downstream ``dict()`` conversion fail opaquely.
    """
    if not isinstance(data, dict):
        raise TypeError(  # noqa: TRY003
            f"Slack method {method} returned non-dict data "
            f"({type(data).__name__}); expected a JSON object."
        )
    return data


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
        """Call an official Slack Web API method via slack_sdk.

        Scalar-only params are form-encoded. If any value is a ``dict`` or
        ``list``, the whole call is sent as a JSON body instead: aiohttp's form
        encoder mangles nested structures (a dict serializes to its first key, a
        list of dicts to a Python ``repr``), whereas Slack accepts JSON bodies
        for these methods — which is what slack_sdk's own typed methods send.
        """
        clean = _drop_none(kwargs)
        if any(isinstance(v, (dict, list)) for v in clean.values()):
            response = await self.web_client.api_call(method, json=clean)
        else:
            response = await self.web_client.api_call(method, data=clean)
        return _require_dict(response.data, method)

    async def api_call_json(self, method: str, **kwargs) -> dict:
        """Call an official Slack Web API method via slack_sdk (JSON body).

        Some methods (e.g. files.completeUploadExternal) require complex
        nested objects that must be sent as JSON rather than form-encoded.
        """
        response = await self.web_client.api_call(method, json=_drop_none(kwargs))
        return _require_dict(response.data, method)

    async def files_upload_v2(self, **kwargs) -> dict:
        """Upload a file via slack_sdk's ``files_upload_v2`` helper.

        ``files.upload.v2`` is not a real HTTP method — it is an SDK helper that
        runs the ``files.getUploadURLExternal`` -> upload-to-URL ->
        ``files.completeUploadExternal`` flow. Delegate to it rather than POSTing
        the bogus method name.
        """
        response = await self.web_client.files_upload_v2(**_drop_none(kwargs))
        return _require_dict(response.data, "files.upload.v2")

    async def users_set_photo(self, **kwargs) -> dict:
        """Set the user profile photo via slack_sdk's multipart helper.

        ``users.setPhoto`` is a binary multipart upload; delegate to the SDK
        method (which builds the multipart body) rather than form-encoding.
        """
        response = await self.web_client.users_setPhoto(**_drop_none(kwargs))
        return _require_dict(response.data, "users.setPhoto")

    def _require_session_tokens(self) -> None:
        if not self.xoxc_token or not self.xoxd_token:
            raise ValueError(  # noqa: TRY003
                "Session tokens (SLACK_XOXC_TOKEN and SLACK_XOXD_TOKEN) are required "
                "for undocumented endpoints. Grab them from your browser cookies while "
                "logged into slack.com."
            )

    def _check_session_response(self, data: dict, method: str) -> dict:
        if not data.get("ok"):
            error = data.get("error", "unknown_error")
            if is_auth_failure(error):
                raise ValueError(  # noqa: TRY003
                    f"Session endpoint {method} failed: {error}. "
                    "Your xoxc/xoxd tokens may be expired — re-grab them "
                    "from browser cookies while logged into slack.com."
                )
        return data

    async def session_call(self, method: str, **kwargs) -> dict:
        """Call an undocumented Slack endpoint using xoxc + xoxd auth."""
        self._require_session_tokens()
        resp = await self.session_client.post(method, json=_drop_none(kwargs))
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
            data=_drop_none(kwargs),
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
