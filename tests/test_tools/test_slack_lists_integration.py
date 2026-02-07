import time

import pytest

from slack_mcp.tools.auth import auth_test
from slack_mcp.tools.slack_lists import (
    slack_lists_access_delete,
    slack_lists_access_set,
    slack_lists_create,
    slack_lists_download_get,
    slack_lists_download_start,
    slack_lists_items_create,
    slack_lists_items_delete,
    slack_lists_items_delete_multiple,
    slack_lists_items_info,
    slack_lists_items_list,
    slack_lists_items_update,
    slack_lists_update,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_slack_lists_lifecycle_live(live_client):
    """Create a list, exercise all operations, clean up."""
    auth = await auth_test(client=live_client)
    user_id = auth["user_id"]

    # Step 1: Create list
    created = await slack_lists_create(
        name="Integration Test List",
        description="Created by integration test",
        client=live_client,
    )
    assert created["ok"] is True
    list_id = created["list_id"]

    # Step 2: Update list name
    updated = await slack_lists_update(
        list_id=list_id,
        name="Renamed Integration Test List",
        client=live_client,
    )
    assert updated["ok"] is True

    # Step 3: Access set (own user — returns ok)
    access_set = await slack_lists_access_set(
        list_id=list_id,
        access_level="write",
        user_ids=[user_id],
        client=live_client,
    )
    assert access_set["ok"] is True

    # Step 4: Access delete (own user — returns ok)
    access_del = await slack_lists_access_delete(
        list_id=list_id,
        user_ids=[user_id],
        client=live_client,
    )
    assert access_del["ok"] is True

    # Step 5: Create a list item
    item_created = await slack_lists_items_create(
        list_id=list_id,
        client=live_client,
    )
    assert item_created["ok"] is True
    item_id = item_created["item"]["id"]

    # Step 6: List items
    items = await slack_lists_items_list(list_id=list_id, client=live_client)
    assert items["ok"] is True

    # Step 7: Get item info
    item_info = await slack_lists_items_info(
        item_id=item_id, list_id=list_id, client=live_client
    )
    assert item_info["ok"] is True

    # Step 8: Delete item
    item_deleted = await slack_lists_items_delete(
        item_id=item_id, list_id=list_id, client=live_client
    )
    assert item_deleted["ok"] is True

    # Step 9: Create two items and delete multiple
    item_a = await slack_lists_items_create(list_id=list_id, client=live_client)
    item_b = await slack_lists_items_create(list_id=list_id, client=live_client)
    id_a = item_a["item"]["id"]
    id_b = item_b["item"]["id"]

    multi_del = await slack_lists_items_delete_multiple(
        item_ids=[id_a, id_b], list_id=list_id, client=live_client
    )
    assert multi_del["ok"] is True

    # Step 10: Download start then get
    dl_start = await slack_lists_download_start(list_id=list_id, client=live_client)
    assert dl_start["ok"] is True
    job_id = dl_start["job_id"]

    time.sleep(2)

    dl_get = await slack_lists_download_get(
        job_id=job_id, list_id=list_id, client=live_client
    )
    assert dl_get["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="undocumented cells format for items.update")
async def test_slack_lists_items_update_live(live_client):
    pass
