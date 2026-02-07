import pytest

from slack_mcp.tools.conversations import (
    conversations_accept_shared_invite,
    conversations_approve_shared_invite,
    conversations_archive,
    conversations_canvases_create,
    conversations_close,
    conversations_create,
    conversations_decline_shared_invite,
    conversations_external_invite_permissions_set,
    conversations_history,
    conversations_info,
    conversations_invite,
    conversations_invite_shared,
    conversations_join,
    conversations_kick,
    conversations_leave,
    conversations_list,
    conversations_list_connect_invites,
    conversations_mark,
    conversations_members,
    conversations_open,
    conversations_rename,
    conversations_replies,
    conversations_request_shared_invite_approve,
    conversations_request_shared_invite_deny,
    conversations_request_shared_invite_list,
    conversations_set_purpose,
    conversations_set_topic,
    conversations_unarchive,
)


@pytest.mark.asyncio
async def test_conversations_accept_shared_invite(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_accept_shared_invite(
        channel_name="test-channel", invite_id="I123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.acceptSharedInvite",
        channel_name="test-channel",
        invite_id="I123",
    )


@pytest.mark.asyncio
async def test_conversations_approve_shared_invite(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_approve_shared_invite(
        invite_id="I123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.approveSharedInvite", invite_id="I123"
    )


@pytest.mark.asyncio
async def test_conversations_archive(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_archive(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.archive", channel="C123"
    )


@pytest.mark.asyncio
async def test_conversations_canvases_create(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_canvases_create(channel_id="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.canvases.create", channel_id="C123"
    )


@pytest.mark.asyncio
async def test_conversations_close(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_close(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("conversations.close", channel="C123")


@pytest.mark.asyncio
async def test_conversations_create(mock_client):
    mock_client.api_call.return_value = {"ok": True, "channel": {"id": "C456"}}
    result = await conversations_create(name="test-channel", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.create", name="test-channel"
    )


@pytest.mark.asyncio
async def test_conversations_decline_shared_invite(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_decline_shared_invite(
        invite_id="I123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.declineSharedInvite", invite_id="I123"
    )


@pytest.mark.asyncio
async def test_conversations_external_invite_permissions_set(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_external_invite_permissions_set(
        channel="C123", action="upgrade", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.externalInvitePermissions.set",
        channel="C123",
        action="upgrade",
    )


@pytest.mark.asyncio
async def test_conversations_history(mock_client):
    mock_client.api_call.return_value = {"ok": True, "messages": []}
    result = await conversations_history(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.history", channel="C123"
    )


@pytest.mark.asyncio
async def test_conversations_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "channel": {}}
    result = await conversations_info(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("conversations.info", channel="C123")


@pytest.mark.asyncio
async def test_conversations_invite(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_invite(
        channel="C123", users="U123,U456", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.invite", channel="C123", users="U123,U456"
    )


@pytest.mark.asyncio
async def test_conversations_invite_shared(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_invite_shared(
        channel="C123", emails=["test@example.com"], client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.inviteShared",
        channel="C123",
        emails=["test@example.com"],
    )


@pytest.mark.asyncio
async def test_conversations_join(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_join(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("conversations.join", channel="C123")


@pytest.mark.asyncio
async def test_conversations_kick(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_kick(channel="C123", user="U123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.kick", channel="C123", user="U123"
    )


@pytest.mark.asyncio
async def test_conversations_leave(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_leave(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("conversations.leave", channel="C123")


@pytest.mark.asyncio
async def test_conversations_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "channels": []}
    result = await conversations_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("conversations.list")


@pytest.mark.asyncio
async def test_conversations_list_connect_invites(mock_client):
    mock_client.api_call.return_value = {"ok": True, "invites": []}
    result = await conversations_list_connect_invites(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("conversations.listConnectInvites")


@pytest.mark.asyncio
async def test_conversations_mark(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_mark(
        channel="C123", ts="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.mark", channel="C123", ts="1234.5678"
    )


@pytest.mark.asyncio
async def test_conversations_members(mock_client):
    mock_client.api_call.return_value = {"ok": True, "members": ["U123"]}
    result = await conversations_members(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.members", channel="C123"
    )


@pytest.mark.asyncio
async def test_conversations_open(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_open(users="U123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("conversations.open", users="U123")


@pytest.mark.asyncio
async def test_conversations_rename(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_rename(
        channel="C123", name="new-name", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.rename", channel="C123", name="new-name"
    )


@pytest.mark.asyncio
async def test_conversations_replies(mock_client):
    mock_client.api_call.return_value = {"ok": True, "messages": []}
    result = await conversations_replies(
        channel="C123", ts="1234.5678", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.replies", channel="C123", ts="1234.5678"
    )


@pytest.mark.asyncio
async def test_conversations_request_shared_invite_approve(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_request_shared_invite_approve(
        invite_id="I123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.requestSharedInvite.approve", invite_id="I123"
    )


@pytest.mark.asyncio
async def test_conversations_request_shared_invite_deny(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_request_shared_invite_deny(
        invite_id="I123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.requestSharedInvite.deny", invite_id="I123"
    )


@pytest.mark.asyncio
async def test_conversations_request_shared_invite_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "invites": []}
    result = await conversations_request_shared_invite_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.requestSharedInvite.list"
    )


@pytest.mark.asyncio
async def test_conversations_set_purpose(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_set_purpose(
        channel="C123", purpose="Test purpose", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.setPurpose", channel="C123", purpose="Test purpose"
    )


@pytest.mark.asyncio
async def test_conversations_set_topic(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_set_topic(
        channel="C123", topic="Test topic", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.setTopic", channel="C123", topic="Test topic"
    )


@pytest.mark.asyncio
async def test_conversations_unarchive(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await conversations_unarchive(channel="C123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "conversations.unarchive", channel="C123"
    )
