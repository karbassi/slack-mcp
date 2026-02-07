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


@pytest.mark.asyncio
async def test_files_comments_delete(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await files_comments_delete(file="F123", id="Fc123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "files.comments.delete", file="F123", id="Fc123"
    )


@pytest.mark.asyncio
async def test_files_complete_upload_external(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    files = [{"id": "F123", "title": "test.txt"}]
    result = await files_complete_upload_external(files=files, client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "files.completeUploadExternal", files=files
    )


@pytest.mark.asyncio
async def test_files_delete(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await files_delete(file="F123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("files.delete", file="F123")


@pytest.mark.asyncio
async def test_files_get_upload_url_external(mock_client):
    mock_client.api_call.return_value = {"ok": True, "upload_url": "https://..."}
    result = await files_get_upload_url_external(
        filename="test.txt", length=100, client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "files.getUploadURLExternal", filename="test.txt", length=100
    )


@pytest.mark.asyncio
async def test_files_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "file": {}}
    result = await files_info(file="F123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("files.info", file="F123")


@pytest.mark.asyncio
async def test_files_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "files": []}
    result = await files_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("files.list")


@pytest.mark.asyncio
async def test_files_remote_add(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await files_remote_add(
        external_id="ext123",
        external_url="https://example.com/file",
        title="Test File",
        client=mock_client,
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "files.remote.add",
        external_id="ext123",
        external_url="https://example.com/file",
        title="Test File",
    )


@pytest.mark.asyncio
async def test_files_remote_info(mock_client):
    mock_client.api_call.return_value = {"ok": True, "file": {}}
    result = await files_remote_info(file="F123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("files.remote.info", file="F123")


@pytest.mark.asyncio
async def test_files_remote_list(mock_client):
    mock_client.api_call.return_value = {"ok": True, "files": []}
    result = await files_remote_list(client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("files.remote.list")


@pytest.mark.asyncio
async def test_files_remote_remove(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await files_remote_remove(file="F123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("files.remote.remove", file="F123")


@pytest.mark.asyncio
async def test_files_remote_share(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await files_remote_share(
        channels="C123", file="F123", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "files.remote.share", channels="C123", file="F123"
    )


@pytest.mark.asyncio
async def test_files_remote_update(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await files_remote_update(file="F123", title="Updated", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "files.remote.update", file="F123", title="Updated"
    )


@pytest.mark.asyncio
async def test_files_revoke_public_url(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await files_revoke_public_url(file="F123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("files.revokePublicURL", file="F123")


@pytest.mark.asyncio
async def test_files_shared_public_url(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await files_shared_public_url(file="F123", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with("files.sharedPublicURL", file="F123")


@pytest.mark.asyncio
async def test_files_upload(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await files_upload(content="hello", filename="test.txt", client=mock_client)
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "files.upload", content="hello", filename="test.txt"
    )


@pytest.mark.asyncio
async def test_files_upload_v2(mock_client):
    mock_client.api_call.return_value = {"ok": True}
    result = await files_upload_v2(
        content="hello", filename="test.txt", client=mock_client
    )
    assert result["ok"] is True
    mock_client.api_call.assert_called_once_with(
        "files.upload.v2", content="hello", filename="test.txt"
    )
