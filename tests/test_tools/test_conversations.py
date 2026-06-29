from slack_sdk.errors import SlackApiError

from slack_mcp.compact import compact_channel_list, compact_message_list, get_compactor
from tests.conftest import assert_api_call


async def test_conversations_accept_shared_invite(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_accept_shared_invite",
        {"channel_name": "test-channel", "invite_id": "I123"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "conversations.acceptSharedInvite",
        channel_name="test-channel",
        invite_id="I123",
    )


async def test_conversations_approve_shared_invite(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_approve_shared_invite", {"invite_id": "I123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "conversations.approveSharedInvite", invite_id="I123"
    )


async def test_conversations_archive(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_archive", {"channel": "C123"}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.archive", channel="C123")


async def test_conversations_canvases_create(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_canvases_create", {"channel_id": "C123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "conversations.canvases.create", channel_id="C123"
    )


async def test_conversations_close(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_close", {"channel": "C123"}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.close", channel="C123")


async def test_conversations_create(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "channel": {"id": "C456"}}
    result = await mcp_client.call_tool(
        "conversations_create", {"name": "test-channel"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "conversations.create", name="test-channel"
    )


async def test_conversations_decline_shared_invite(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_decline_shared_invite", {"invite_id": "I123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "conversations.declineSharedInvite", invite_id="I123"
    )


async def test_conversations_external_invite_permissions_set(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_external_invite_permissions_set",
        {"channel": "C123", "action": "upgrade", "target_team": "T999"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "conversations.externalInvitePermissions.set",
        channel="C123",
        action="upgrade",
        target_team="T999",
    )


async def test_conversations_history(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "messages": []}
    result = await mcp_client.call_tool(
        "conversations_history", {"channel": "C123"}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.history", channel="C123")


async def test_conversations_info(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "channel": {}}
    result = await mcp_client.call_tool(
        "conversations_info", {"channel": "C123"}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.info", channel="C123")


async def test_conversations_invite(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_invite", {"channel": "C123", "users": "U123,U456"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "conversations.invite",
        channel="C123",
        users="U123,U456",
    )


async def test_conversations_invite_shared(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_invite_shared",
        {"channel": "C123", "emails": ["test@example.com"]},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "conversations.inviteShared",
        channel="C123",
        emails=["test@example.com"],
    )


async def test_conversations_join(mcp_client, slack_stub):
    result = await mcp_client.call_tool("conversations_join", {"channel": "C123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.join", channel="C123")


async def test_conversations_kick(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_kick", {"channel": "C123", "user": "U123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "conversations.kick", channel="C123", user="U123"
    )


async def test_conversations_leave(mcp_client, slack_stub):
    result = await mcp_client.call_tool("conversations_leave", {"channel": "C123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.leave", channel="C123")


async def test_conversations_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "channels": []}
    result = await mcp_client.call_tool("conversations_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.list")


async def test_conversations_list_connect_invites(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "invites": []}
    result = await mcp_client.call_tool("conversations_list_connect_invites", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.listConnectInvites")


async def test_conversations_mark(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_mark", {"channel": "C123", "ts": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "conversations.mark", channel="C123", ts="1234.5678"
    )


async def test_conversations_mark_missing_scope_fallback(mcp_client, slack_stub):
    """When api_call raises missing_scope, the tool falls back to session_call_form."""
    slack_stub.api_call.side_effect = SlackApiError(
        message="missing_scope",
        response={"ok": False, "error": "missing_scope"},
    )
    await mcp_client.call_tool(
        "conversations_mark",
        {"channel": "C123", "ts": "1234.5678"},
        raise_on_error=False,
    )
    slack_stub.session_call_form.assert_called_once()
    args, kwargs = slack_stub.session_call_form.call_args
    assert args[0] == "conversations.mark"
    assert kwargs.get("channel") == "C123"
    assert kwargs.get("ts") == "1234.5678"


async def test_conversations_members(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "members": ["U123"]}
    result = await mcp_client.call_tool(
        "conversations_members", {"channel": "C123"}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.members", channel="C123")


async def test_conversations_open(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_open", {"users": "U123"}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.open", users="U123")


async def test_conversations_rename(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_rename", {"channel": "C123", "name": "new-name"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "conversations.rename", channel="C123", name="new-name"
    )


async def test_conversations_replies(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "messages": []}
    result = await mcp_client.call_tool(
        "conversations_replies", {"channel": "C123", "ts": "1234.5678"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "conversations.replies",
        channel="C123",
        ts="1234.5678",
    )


async def test_conversations_request_shared_invite_approve(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_request_shared_invite_approve",
        {"invite_id": "I123", "is_external_limited": True},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "conversations.requestSharedInvite.approve",
        invite_id="I123",
        is_external_limited=True,
    )


async def test_conversations_request_shared_invite_deny(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_request_shared_invite_deny",
        {"invite_id": "I123", "message": "not allowed"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "conversations.requestSharedInvite.deny",
        invite_id="I123",
        message="not allowed",
    )


async def test_conversations_request_shared_invite_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "invites": []}
    result = await mcp_client.call_tool(
        "conversations_request_shared_invite_list", {}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.requestSharedInvite.list")


async def test_conversations_set_purpose(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_set_purpose",
        {"channel": "C123", "purpose": "Test purpose"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "conversations.setPurpose",
        channel="C123",
        purpose="Test purpose",
    )


async def test_conversations_set_topic(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_set_topic",
        {"channel": "C123", "topic": "Test topic"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "conversations.setTopic",
        channel="C123",
        topic="Test topic",
    )


async def test_conversations_unarchive(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "conversations_unarchive", {"channel": "C123"}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "conversations.unarchive", channel="C123")


def test_conversations_history_compactable():
    assert get_compactor("conversations_history") is compact_message_list


def test_conversations_replies_compactable():
    assert get_compactor("conversations_replies") is compact_message_list


def test_conversations_list_compactable():
    assert get_compactor("conversations_list") is compact_channel_list
