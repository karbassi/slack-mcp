from tests.conftest import assert_api_call


async def test_canvases_access_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "canvases_access_delete", {"canvas_id": "F123", "user_ids": ["U123"]}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "canvases.access.delete",
        canvas_id="F123",
        user_ids=["U123"],
    )


async def test_canvases_access_set(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "canvases_access_set",
        {"canvas_id": "F123", "access_level": "write", "user_ids": ["U123"]},
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "canvases.access.set",
        canvas_id="F123",
        access_level="write",
        user_ids=["U123"],
    )


async def test_canvases_create(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "canvases_create", {"title": "Test Canvas"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json, "canvases.create", title="Test Canvas"
    )


async def test_canvases_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool("canvases_delete", {"canvas_id": "F123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "canvases.delete", canvas_id="F123")


async def test_canvases_edit(mcp_client, slack_stub):
    changes = [
        {
            "operation": "insert_at_end",
            "document_content": {"type": "markdown", "markdown": "hi"},
        }
    ]
    result = await mcp_client.call_tool(
        "canvases_edit", {"canvas_id": "F123", "changes": changes}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json, "canvases.edit", canvas_id="F123", changes=changes
    )


async def test_canvases_sections_lookup(mcp_client, slack_stub):
    criteria = {"section_types": ["any_header"]}
    result = await mcp_client.call_tool(
        "canvases_sections_lookup", {"canvas_id": "F123", "criteria": criteria}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json,
        "canvases.sections.lookup",
        canvas_id="F123",
        criteria=criteria,
    )
