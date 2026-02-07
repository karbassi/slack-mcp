import pytest

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
@pytest.mark.skip(reason="destructive: would delete a file comment")
async def test_files_comments_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would complete an upload")
async def test_files_complete_upload_external_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would delete a file")
async def test_files_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would initiate an upload URL")
async def test_files_get_upload_url_external_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a specific file ID")
async def test_files_info_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_files_list_live(live_client):
    result = await files_list(client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would add a remote file")
async def test_files_remote_add_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a specific remote file ID")
async def test_files_remote_info_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires remote files to be configured")
async def test_files_remote_list_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would remove a remote file")
async def test_files_remote_remove_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would share a remote file")
async def test_files_remote_share_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would update a remote file")
async def test_files_remote_update_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would revoke public URL for a file")
async def test_files_revoke_public_url_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would enable public sharing for a file")
async def test_files_shared_public_url_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would upload a file")
async def test_files_upload_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="destructive: would upload a file via v2 API")
async def test_files_upload_v2_live(live_client):
    pass
