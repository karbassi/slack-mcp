import pytest

from slack_mcp.tools.users import (
    users_conversations,
    users_delete_photo,
    users_discoverable_contacts_lookup,
    users_get_presence,
    users_identity,
    users_info,
    users_list,
    users_lookup_by_email,
    users_profile_get,
    users_profile_set,
    users_set_photo,
    users_set_presence,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_users_conversations_live(live_client):
    result = await users_conversations(limit=5, client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would delete the user's profile photo")
async def test_users_delete_photo_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a specific email address")
async def test_users_discoverable_contacts_lookup_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a specific user ID")
async def test_users_get_presence_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires Sign in with Slack scopes")
async def test_users_identity_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a specific user ID")
async def test_users_info_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_users_list_live(live_client):
    result = await users_list(limit=5, client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a specific email address")
async def test_users_lookup_by_email_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="read-only but requires specific user context")
async def test_users_profile_get_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would modify user profile")
async def test_users_profile_set_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would set the user's profile photo")
async def test_users_set_photo_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would change user presence")
async def test_users_set_presence_live(live_client):
    pass
