import pytest

from slack_mcp.tools.resolve import resolve_names


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_own_user_id(live_client):
    auth = await live_client.api_call("auth.test")
    uid = auth["user_id"]

    result = await resolve_names(user_ids=[uid], client=live_client)
    assert result["ok"] is True
    assert result["names"][uid] is not None
