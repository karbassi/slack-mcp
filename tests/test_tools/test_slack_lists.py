from tests.conftest import assert_api_call


async def test_slack_lists_access_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "slack_lists_access_delete", {"list_id": "L123", "user_ids": ["U123"]}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.access.delete",
        list_id="L123",
        user_ids=["U123"],
    )


async def test_slack_lists_access_set(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "slack_lists_access_set", {"list_id": "L123", "access_level": "write"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.access.set",
        list_id="L123",
        access_level="write",
    )


async def test_slack_lists_create(mcp_client, slack_stub):
    schema = [{"key": "Col1", "name": "Title", "type": "text"}]
    desc = [{"type": "rich_text", "elements": []}]
    result = await mcp_client.call_tool(
        "slack_lists_create",
        {"name": "My List", "schema": schema, "description_blocks": desc},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.create",
        name="My List",
        schema=schema,
        description_blocks=desc,
    )


async def test_slack_lists_download_get(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "slack_lists_download_get", {"job_id": "J123", "list_id": "L123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.download.get",
        job_id="J123",
        list_id="L123",
    )


async def test_slack_lists_download_start(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "slack_lists_download_start", {"list_id": "L123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json, "slackLists.download.start", list_id="L123"
    )


async def test_slack_lists_items_create(mcp_client, slack_stub):
    fields = [{"column_id": "Col123", "text": "hi"}]
    result = await mcp_client.call_tool(
        "slack_lists_items_create", {"list_id": "L123", "initial_fields": fields}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.items.create",
        list_id="L123",
        initial_fields=fields,
    )


async def test_slack_lists_items_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "slack_lists_items_delete", {"item_id": "I123", "list_id": "L123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.items.delete",
        id="I123",
        list_id="L123",
    )


async def test_slack_lists_items_delete_multiple(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "slack_lists_items_delete_multiple",
        {"item_ids": ["I1", "I2"], "list_id": "L123"},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.items.deleteMultiple",
        ids=["I1", "I2"],
        list_id="L123",
    )


async def test_slack_lists_items_info(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "slack_lists_items_info", {"item_id": "I123", "list_id": "L123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.items.info",
        id="I123",
        list_id="L123",
    )


async def test_slack_lists_items_list(mcp_client, slack_stub):
    slack_stub.api_call_json.return_value = {"ok": True, "items": []}
    result = await mcp_client.call_tool(
        "slack_lists_items_list", {"list_id": "L123", "archived": True}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.items.list",
        list_id="L123",
        archived=True,
    )


async def test_slack_lists_items_update(mcp_client, slack_stub):
    cells = [{"row_id": "Rec123", "column_id": "Col123", "text": "new"}]
    result = await mcp_client.call_tool(
        "slack_lists_items_update", {"list_id": "L123", "cells": cells}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.items.update",
        list_id="L123",
        cells=cells,
    )


async def test_slack_lists_update(mcp_client, slack_stub):
    desc = [{"type": "rich_text", "elements": []}]
    result = await mcp_client.call_tool(
        "slack_lists_update",
        {"list_id": "L123", "name": "Updated", "description_blocks": desc},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "slackLists.update",
        id="L123",
        name="Updated",
        description_blocks=desc,
    )
