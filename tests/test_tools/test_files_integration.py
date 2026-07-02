import uuid

import httpx
import pytest

from slack_mcp.tools.conversations import conversations_archive, conversations_create
from slack_mcp.tools.files import (
    files_comments_delete,
    files_complete_upload_external,
    files_delete,
    files_favorites_list,
    files_get_shares,
    files_get_upload_url_external,
    files_info,
    files_list,
    files_recently_deleted,
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
@pytest.mark.usefixtures("requires_session_tokens")
async def test_files_recently_deleted_live(live_client):
    result = await files_recently_deleted(client=live_client)
    assert result["ok"] is True
    assert "files" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.usefixtures("requires_session_tokens")
async def test_files_favorites_list_live(live_client):
    result = await files_favorites_list(type="all", client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.usefixtures("requires_session_tokens")
async def test_files_get_shares_live(live_client):
    listing = await files_list(client=live_client)
    assert listing["ok"] is True
    files = listing.get("files") or []
    if not files:
        pytest.skip("workspace has no files to look up shares for")
    result = await files_get_shares(file_id=files[0]["id"], client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="destructive: mutates a live Slack workspace as the token owner; "
    "enable only against a dedicated throwaway workspace"
)
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
    """Legacy upload — deprecated by Slack in favour of the v2 flow."""
    result = await files_upload(
        content="legacy upload test",
        filename="legacy.txt",
        title="Legacy Upload",
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="covered by v2 upload lifecycle test above")
async def test_files_upload_v2_live(live_client):
    """files.upload.v2 — already exercised by test_files_v2_upload_lifecycle_live."""
    result = await files_upload_v2(
        content="v2 upload test",
        filename="v2test.txt",
        title="V2 Upload",
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="not_allowed_token_type: files.remote.add requires bot token (xoxb)"
)
async def test_files_remote_add_live(live_client):
    """Add a remote file reference."""
    ext_id = f"integ-test-{uuid.uuid4().hex[:8]}"
    result = await files_remote_add(
        external_id=ext_id,
        external_url="https://example.com/test.txt",
        title="Remote Test File",
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="not_allowed_token_type: files.remote.info requires bot token (xoxb)"
)
async def test_files_remote_info_live(live_client):
    """Get info about a remote file by external_id."""
    result = await files_remote_info(
        external_id="integ-test-placeholder",
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="not_allowed_token_type: files.remote.list requires bot token (xoxb)"
)
async def test_files_remote_list_live(live_client):
    """List remote files."""
    result = await files_remote_list(client=live_client)
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="not_allowed_token_type: files.remote.remove requires bot token (xoxb)"
)
async def test_files_remote_remove_live(live_client):
    """Remove a remote file."""
    result = await files_remote_remove(
        external_id="integ-test-placeholder",
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="not_allowed_token_type: files.remote.share requires bot token (xoxb)"
)
async def test_files_remote_share_live(live_client):
    """Share a remote file into a channel."""
    result = await files_remote_share(
        channels="C0000000000",
        external_id="integ-test-placeholder",
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(
    reason="not_allowed_token_type: files.remote.update requires bot token (xoxb)"
)
async def test_files_remote_update_live(live_client):
    """Update a remote file."""
    result = await files_remote_update(
        external_id="integ-test-placeholder",
        title="Updated Remote File",
        client=live_client,
    )
    assert "ok" in result


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a file with comments")
async def test_files_comments_delete_live(live_client):
    pass
