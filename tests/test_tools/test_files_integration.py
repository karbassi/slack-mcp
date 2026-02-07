import uuid

import httpx
import pytest

from slack_mcp.tools.conversations import conversations_archive, conversations_create
from slack_mcp.tools.files import (
    files_comments_delete,
    files_complete_upload_external,
    files_delete,
    files_get_upload_url_external,
    files_info,
    files_list,
    files_remote_add,
    files_remote_info,
    files_remote_list,
    files_remote_remove,
    files_remote_share,
    files_remote_update,
    files_revoke_public_url,
    files_shared_public_url,
    files_upload,
    files_upload_v2,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_files_list_live(live_client):
    result = await files_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_files_v2_upload_lifecycle_live(live_client):
    """Upload via v2 flow, get info, toggle public URL, then delete."""
    content = b"integration test file content"

    # Step 1: Get upload URL
    url_result = await files_get_upload_url_external(
        filename="test.txt", length=len(content), client=live_client
    )
    assert url_result["ok"] is True
    upload_url = url_result["upload_url"]
    file_id = url_result["file_id"]

    # Step 2: Upload content to the URL
    async with httpx.AsyncClient() as http:
        resp = await http.post(upload_url, content=content)
        assert resp.status_code == 200

    # Step 3: Complete the upload
    completed = await files_complete_upload_external(
        files=[{"id": file_id, "title": "Test Upload"}], client=live_client
    )
    assert completed["ok"] is True
    uploaded_file_id = completed["files"][0]["id"]

    # Step 4: Get file info
    info = await files_info(file=uploaded_file_id, client=live_client)
    assert info["ok"] is True

    # Step 5: Share public URL
    shared = await files_shared_public_url(file=uploaded_file_id, client=live_client)
    assert shared["ok"] is True

    # Step 6: Revoke public URL
    revoked = await files_revoke_public_url(file=uploaded_file_id, client=live_client)
    assert revoked["ok"] is True

    # Step 7: Delete file
    deleted = await files_delete(file=uploaded_file_id, client=live_client)
    assert deleted["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="method_deprecated: files.upload replaced by v2 flow")
async def test_files_upload_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: files.remote.* requires bot token (xoxb)")
async def test_files_remote_lifecycle_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a file with comments")
async def test_files_comments_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="covered by v2 upload lifecycle test")
async def test_files_upload_v2_live(live_client):
    pass
