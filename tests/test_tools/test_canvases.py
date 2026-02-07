import pytest

from slack_mcp.tools.canvases import (
    canvases_access_delete,
    canvases_access_set,
    canvases_create,
    canvases_delete,
    canvases_edit,
    canvases_sections_lookup,
)


@pytest.mark.asyncio
async def test_canvases_access_delete(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await canvases_access_delete(
        canvas_id="F123", user_ids=["U123"], client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "canvases.access.delete", canvas_id="F123", user_ids=["U123"]
    )


@pytest.mark.asyncio
async def test_canvases_access_set(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await canvases_access_set(
        canvas_id="F123", access_level="write", user_ids=["U123"], client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "canvases.access.set",
        canvas_id="F123",
        access_level="write",
        user_ids=["U123"],
    )


@pytest.mark.asyncio
async def test_canvases_create(mock_client):
    mock_client.api_call.return_value = {"ok": True, "canvas_id": "F123"}
    result = await canvases_create(title="Test Canvas", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "canvases.create", title="Test Canvas"
    )


@pytest.mark.asyncio
async def test_canvases_delete(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await canvases_delete(canvas_id="F123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("canvases.delete", canvas_id="F123")


@pytest.mark.asyncio
async def test_canvases_edit(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    changes = [{"operation": "insert_at_end", "document_content": {"markdown": "hi"}}]
    result = await canvases_edit(
        canvas_id="F123", changes=changes, client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "canvases.edit", canvas_id="F123", changes=changes
    )


@pytest.mark.asyncio
async def test_canvases_sections_lookup(mock_client):
    mock_client.api_call.return_value = {"ok": True, "sections": []}
    criteria = {"section_types": ["any_header"]}
    result = await canvases_sections_lookup(
        canvas_id="F123", criteria=criteria, client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "canvases.sections.lookup", canvas_id="F123", criteria=criteria
    )
