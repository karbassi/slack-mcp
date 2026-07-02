import contextlib
import time

import pytest
from slack_sdk.errors import SlackApiError

from slack_mcp.tools.reminders import (
    reminders_add,
    reminders_complete,
    reminders_delete,
    reminders_info,
    reminders_list,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_reminders_list_live(live_client):
    result = await reminders_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="destructive: mutates a live Slack workspace as the token owner; "
    "enable only against a dedicated throwaway workspace"
)
async def test_reminders_add_live(live_client):
    """Create a reminder; the reminders_delete cleanup does not clear it from
    Slack's "Later" view, so this leaves state behind."""
    added = await reminders_add(
        text="integration test reminder", time="in 1 hour", client=live_client
    )
    assert added["ok"] is True
    with contextlib.suppress(SlackApiError, KeyError):
        await reminders_delete(reminder=added["reminder"]["id"], client=live_client)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="destructive: mutates a live Slack workspace as the token owner; "
    "enable only against a dedicated throwaway workspace"
)
async def test_reminders_info_live(live_client):
    """Create a reminder and retrieve its info."""
    post_at = int(time.time()) + 3600
    added = await reminders_add(
        text="info test reminder", time=str(post_at), client=live_client
    )
    assert added["ok"] is True
    reminder_id = added["reminder"]["id"]

    try:
        info = await reminders_info(reminder=reminder_id, client=live_client)
        assert info["ok"] is True
        assert info["reminder"]["id"] == reminder_id
    except SlackApiError as e:
        # Some token types return not_found for reminders.info
        assert e.response["error"] in ("not_found", "not_allowed_token_type")  # noqa: PT017
    finally:
        with contextlib.suppress(SlackApiError):
            await reminders_delete(reminder=reminder_id, client=live_client)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="destructive: mutates a live Slack workspace as the token owner; "
    "enable only against a dedicated throwaway workspace"
)
async def test_reminders_complete_live(live_client):
    """Create a reminder and mark it as complete."""
    post_at = int(time.time()) + 3600
    added = await reminders_add(
        text="complete test reminder", time=str(post_at), client=live_client
    )
    assert added["ok"] is True
    reminder_id = added["reminder"]["id"]

    try:
        result = await reminders_complete(reminder=reminder_id, client=live_client)
        assert result["ok"] is True
    except SlackApiError as e:
        # Some token types return not_found for reminders.complete
        assert e.response["error"] in ("not_found", "not_allowed_token_type")  # noqa: PT017
    finally:
        with contextlib.suppress(SlackApiError):
            await reminders_delete(reminder=reminder_id, client=live_client)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="destructive: mutates a live Slack workspace as the token owner; "
    "enable only against a dedicated throwaway workspace"
)
async def test_reminders_delete_live(live_client):
    """Create a reminder and delete it."""
    post_at = int(time.time()) + 3600
    added = await reminders_add(
        text="delete test reminder", time=str(post_at), client=live_client
    )
    assert added["ok"] is True
    reminder_id = added["reminder"]["id"]

    try:
        result = await reminders_delete(reminder=reminder_id, client=live_client)
        assert result["ok"] is True
    except SlackApiError as e:
        # Some token types return not_found for reminders.delete
        assert e.response["error"] in ("not_found", "not_allowed_token_type")  # noqa: PT017
