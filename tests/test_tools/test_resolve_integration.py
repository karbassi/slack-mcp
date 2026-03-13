import pytest

from slack_mcp.client import get_client
from slack_mcp.tools.resolve import resolve_names


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_own_user_id():
    client = get_client()
    auth = await client.api_call("auth.test")
    uid = auth["user_id"]

    result = await resolve_names(user_ids=[uid], client=client)
    assert result["ok"] is True
    assert result["names"][uid] is not None
