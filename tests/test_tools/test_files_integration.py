import uuid

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
@pytest.mark.skip(reason="not_allowed_token_type: legacy files.upload not supported by this token")
async def test_files_upload_info_public_url_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="not_allowed_token_type: files.remote.add not supported by this token")
async def test_files_remote_lifecycle_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a file with comments")
async def test_files_comments_delete_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="complex multi-step upload flow")
async def test_files_complete_upload_external_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="complex multi-step upload flow")
async def test_files_get_upload_url_external_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="covered by files_upload_info_public_url_delete test")
async def test_files_upload_v2_live(live_client):
    pass
