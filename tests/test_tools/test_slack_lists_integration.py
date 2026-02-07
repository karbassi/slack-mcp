import pytest

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
@pytest.mark.skip(reason="requires a valid list_id")
async def test_slack_lists_access_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid list_id")
async def test_slack_lists_access_set_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would create a list")
async def test_slack_lists_create_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid list_id and download_id")
async def test_slack_lists_download_get_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid list_id")
async def test_slack_lists_download_start_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid list_id")
async def test_slack_lists_items_create_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid list_id and item_id")
async def test_slack_lists_items_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid list_id and item_ids")
async def test_slack_lists_items_delete_multiple_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid list_id and item_id")
async def test_slack_lists_items_info_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid list_id")
async def test_slack_lists_items_list_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid list_id and item_id")
async def test_slack_lists_items_update_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid list_id")
async def test_slack_lists_update_live(live_client):
    pass
