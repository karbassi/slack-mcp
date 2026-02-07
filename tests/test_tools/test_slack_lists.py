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


@pytest.mark.asyncio
async def test_slack_lists_access_delete(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_access_delete(
        list_id="L123", user_ids=["U123"], client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.access.delete", list_id="L123", user_ids=["U123"]
    )


@pytest.mark.asyncio
async def test_slack_lists_access_set(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_access_set(
        list_id="L123", access_level="write", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.access.set", list_id="L123", access_level="write"
    )


@pytest.mark.asyncio
async def test_slack_lists_create(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_create(name="My List", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.create", name="My List"
    )


@pytest.mark.asyncio
async def test_slack_lists_download_get(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_download_get(
        job_id="J123", list_id="L123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.download.get", job_id="J123", list_id="L123"
    )


@pytest.mark.asyncio
async def test_slack_lists_download_start(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_download_start(list_id="L123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.download.start", list_id="L123"
    )


@pytest.mark.asyncio
async def test_slack_lists_items_create(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_items_create(list_id="L123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.items.create", list_id="L123"
    )


@pytest.mark.asyncio
async def test_slack_lists_items_delete(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_items_delete(
        item_id="I123", list_id="L123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.items.delete", id="I123", list_id="L123"
    )


@pytest.mark.asyncio
async def test_slack_lists_items_delete_multiple(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_items_delete_multiple(
        item_ids=["I1", "I2"], list_id="L123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.items.deleteMultiple", ids=["I1", "I2"], list_id="L123"
    )


@pytest.mark.asyncio
async def test_slack_lists_items_info(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_items_info(
        item_id="I123", list_id="L123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.items.info", id="I123", list_id="L123"
    )


@pytest.mark.asyncio
async def test_slack_lists_items_list(mock_client):
    mock_client.api_call_json.return_value = {"ok": True, "items": []}
    result = await slack_lists_items_list(list_id="L123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.items.list", list_id="L123"
    )


@pytest.mark.asyncio
async def test_slack_lists_items_update(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_items_update(
        item_id="I123", list_id="L123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.items.update", id="I123", list_id="L123"
    )


@pytest.mark.asyncio
async def test_slack_lists_update(mock_client):
    mock_client.api_call_json.return_value = {"ok": True}
    result = await slack_lists_update(
        list_id="L123", name="Updated", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call_json.assert_called_once_with(
        "slackLists.update", id="L123", name="Updated"
    )
