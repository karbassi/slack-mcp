import json
import uuid

import pytest

from slack_mcp.tools.auth import auth_test
from slack_mcp.tools.calls import (
    calls_add,
    calls_end,
    calls_info,
    calls_participants_add,
    calls_participants_remove,
    calls_update,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="destructive: mutates a live Slack workspace as the token owner; "
    "enable only against a dedicated throwaway workspace"
)
async def test_calls_lifecycle_live(live_client):
    """Register a call, get info, update it, then end it."""
    ext_id = f"test-call-{uuid.uuid4().hex[:8]}"

    # Add call
    added = await calls_add(
        external_unique_id=ext_id,
        join_url="https://example.com/call",
        title="Integration Test Call",
        client=live_client,
    )
    assert added["ok"] is True
    call_id = added["call"]["id"]

    # Info
    info = await calls_info(id=call_id, client=live_client)
    assert info["ok"] is True

    # Update
    updated = await calls_update(
        id=call_id, title="Updated Call Title", client=live_client
    )
    assert updated["ok"] is True

    # End call
    ended = await calls_end(id=call_id, client=live_client)
    assert ended["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="destructive: mutates a live Slack workspace as the token owner; "
    "enable only against a dedicated throwaway workspace"
)
async def test_calls_participants_add_remove_live(live_client):
    """Register a call, add participants, remove them, then end it."""
    ext_id = f"test-call-{uuid.uuid4().hex[:8]}"

    # Add call
    added = await calls_add(
        external_unique_id=ext_id,
        join_url="https://example.com/call",
        title="Participants Test Call",
        client=live_client,
    )
    assert added["ok"] is True
    call_id = added["call"]["id"]

    try:
        # Get our own user ID for a valid participant
        auth = await auth_test(client=live_client)
        user_id = auth["user_id"]

        # Add participants (must be JSON-encoded for form-encoded API call)
        participants = json.dumps(
            [{"external_id": f"ext-{user_id}", "display_name": "Test User"}]
        )
        add_result = await calls_participants_add(
            id=call_id, users=participants, client=live_client
        )
        assert "ok" in add_result

        # Remove participants
        remove_result = await calls_participants_remove(
            id=call_id, users=participants, client=live_client
        )
        assert "ok" in remove_result
    finally:
        await calls_end(id=call_id, client=live_client)
