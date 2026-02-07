import pytest

from slack_mcp.tools.conversations import (
    conversations_history,
    conversations_info,
    conversations_list,
    conversations_list_connect_invites,
    conversations_members,
    conversations_replies,
    conversations_request_shared_invite_list,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_list_live(live_client):
    result = await conversations_list(limit=5, client=live_client)
    assert result["ok"] is True
    assert "channels" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_history_live(live_client):
    # First get a channel to read history from
    list_result = await conversations_list(limit=1, client=live_client)
    if list_result["ok"] and list_result.get("channels"):
        channel_id = list_result["channels"][0]["id"]
        result = await conversations_history(
            channel=channel_id, limit=5, client=live_client
        )
        assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_info_live(live_client):
    list_result = await conversations_list(limit=1, client=live_client)
    if list_result["ok"] and list_result.get("channels"):
        channel_id = list_result["channels"][0]["id"]
        result = await conversations_info(channel=channel_id, client=live_client)
        assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_conversations_members_live(live_client):
    list_result = await conversations_list(limit=1, client=live_client)
    if list_result["ok"] and list_result.get("channels"):
        channel_id = list_result["channels"][0]["id"]
        result = await conversations_members(channel=channel_id, client=live_client)
        assert result["ok"] is True
