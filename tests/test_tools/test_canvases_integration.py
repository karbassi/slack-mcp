import pytest

from slack_mcp.tools.auth import auth_test
from slack_mcp.tools.canvases import (
    canvases_access_delete,
    canvases_access_set,
    canvases_create,
    canvases_delete,
    canvases_edit,
    canvases_sections_lookup,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_canvases_lifecycle_live(live_client):
    """Create a canvas, edit, sections_lookup, access set/delete, then delete."""
    auth = await auth_test(client=live_client)
    user_id = auth["user_id"]

    canvas_id = None
    try:
        # Step 1: Create canvas
        created = await canvases_create(
            title="Integration Test Canvas",
            document_content={
                "type": "markdown",
                "markdown": "# Hello\nThis is an integration test canvas.",
            },
            client=live_client,
        )
        assert created["ok"] is True
        canvas_id = created["canvas_id"]

        # Step 2: Edit canvas — append content
        edited = await canvases_edit(
            canvas_id=canvas_id,
            changes=[
                {
                    "operation": "insert_at_end",
                    "document_content": {
                        "type": "markdown",
                        "markdown": "\n## Section Two\nAppended by test.",
                    },
                }
            ],
            client=live_client,
        )
        assert edited["ok"] is True

        # Step 3: Look up sections (find headers)
        sections = await canvases_sections_lookup(
            canvas_id=canvas_id,
            criteria={"section_types": ["any_header"]},
            client=live_client,
        )
        assert sections["ok"] is True

        # Step 4: Access set (own user — returns ok but fails silently)
        access_set = await canvases_access_set(
            canvas_id=canvas_id,
            access_level="write",
            user_ids=[user_id],
            client=live_client,
        )
        assert access_set["ok"] is True

        # Step 5: Access delete (own user — returns ok but fails silently)
        access_del = await canvases_access_delete(
            canvas_id=canvas_id,
            user_ids=[user_id],
            client=live_client,
        )
        assert access_del["ok"] is True

        # Step 6: Delete canvas
        deleted = await canvases_delete(canvas_id=canvas_id, client=live_client)
        assert deleted["ok"] is True
        canvas_id = None

    finally:
        if canvas_id:
            await canvases_delete(canvas_id=canvas_id, client=live_client)
