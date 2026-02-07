import uuid

import pytest

from slack_mcp.tools.auth import auth_test
from slack_mcp.tools.usergroups import (
    usergroups_create,
    usergroups_disable,
    usergroups_enable,
    usergroups_list,
    usergroups_update,
    usergroups_users_list,
    usergroups_users_update,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_usergroups_list_live(live_client):
    result = await usergroups_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_usergroups_lifecycle_live(live_client):
    """Create a usergroup, update it, manage users, disable it."""
    handle = f"test-{uuid.uuid4().hex[:8]}"

    # Create
    created = await usergroups_create(
        name=f"Test Group {handle}",
        handle=handle,
        description="Integration test group",
        client=live_client,
    )
    assert created["ok"] is True
    ug_id = created["usergroup"]["id"]

    try:
        # Update
        updated = await usergroups_update(
            usergroup=ug_id,
            name=f"Updated Group {handle}",
            client=live_client,
        )
        assert updated["ok"] is True

        # Get our own user ID for users_update
        auth = await auth_test(client=live_client)
        user_id = auth["user_id"]

        # Set users
        users_updated = await usergroups_users_update(
            usergroup=ug_id, users=user_id, client=live_client
        )
        assert users_updated["ok"] is True

        # List users
        users_listed = await usergroups_users_list(usergroup=ug_id, client=live_client)
        assert users_listed["ok"] is True

        # Disable
        disabled = await usergroups_disable(usergroup=ug_id, client=live_client)
        assert disabled["ok"] is True

        # Enable
        enabled = await usergroups_enable(usergroup=ug_id, client=live_client)
        assert enabled["ok"] is True
    finally:
        # Final cleanup: disable the group
        await usergroups_disable(usergroup=ug_id, client=live_client)
