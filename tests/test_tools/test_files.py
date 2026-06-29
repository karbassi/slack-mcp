from slack_mcp.compact import compact_file_list, get_compactor
from tests.conftest import assert_api_call


async def test_files_comments_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "files_comments_delete", {"file": "F123", "id": "Fc123"}
    )
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "files.comments.delete", file="F123", id="Fc123")


async def test_files_complete_upload_external(mcp_client, slack_stub):
    files = [{"id": "F123", "title": "test.txt"}]
    result = await mcp_client.call_tool(
        "files_complete_upload_external", {"files": files}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call_json, "files.completeUploadExternal", files=files
    )


async def test_files_delete(mcp_client, slack_stub):
    result = await mcp_client.call_tool("files_delete", {"file": "F123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "files.delete", file="F123")


async def test_files_get_upload_url_external(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "files_get_upload_url_external", {"filename": "test.txt", "length": 100}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "files.getUploadURLExternal",
        filename="test.txt",
        length=100,
    )


async def test_files_info(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "file": {}}
    result = await mcp_client.call_tool("files_info", {"file": "F123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "files.info", file="F123")


async def test_files_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "files": []}
    result = await mcp_client.call_tool("files_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "files.list")


async def test_files_remote_add(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "files_remote_add",
        {
            "external_id": "ext123",
            "external_url": "https://example.com/file",
            "title": "Test File",
        },
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call,
        "files.remote.add",
        external_id="ext123",
        external_url="https://example.com/file",
        title="Test File",
    )


async def test_files_remote_info(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "file": {}}
    result = await mcp_client.call_tool("files_remote_info", {"file": "F123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "files.remote.info", file="F123")


async def test_files_remote_list(mcp_client, slack_stub):
    slack_stub.api_call.return_value = {"ok": True, "files": []}
    result = await mcp_client.call_tool("files_remote_list", {})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "files.remote.list")


async def test_files_remote_remove(mcp_client, slack_stub):
    result = await mcp_client.call_tool("files_remote_remove", {"file": "F123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "files.remote.remove", file="F123")


async def test_files_remote_share(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "files_remote_share", {"channels": "C123", "file": "F123"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "files.remote.share", channels="C123", file="F123"
    )


async def test_files_remote_update(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "files_remote_update", {"file": "F123", "title": "Updated"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "files.remote.update", file="F123", title="Updated"
    )


async def test_files_revoke_public_url(mcp_client, slack_stub):
    result = await mcp_client.call_tool("files_revoke_public_url", {"file": "F123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "files.revokePublicURL", file="F123")


async def test_files_shared_public_url(mcp_client, slack_stub):
    result = await mcp_client.call_tool("files_shared_public_url", {"file": "F123"})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "files.sharedPublicURL", file="F123")


async def test_files_upload(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "files_upload", {"content": "hello", "filename": "test.txt"}
    )
    assert result.is_error is False
    assert_api_call(
        slack_stub.api_call, "files.upload", content="hello", filename="test.txt"
    )


async def test_files_upload_v2(mcp_client, slack_stub):
    result = await mcp_client.call_tool(
        "files_upload_v2", {"content": "hello", "filename": "test.txt"}
    )
    assert result.is_error is False
    # Delegates to slack_sdk's files_upload_v2 helper (real getUploadURL ->
    # PUT -> complete flow), not the bogus files.upload.v2 HTTP method.
    slack_stub.files_upload_v2.assert_called_once()
    _, kwargs = slack_stub.files_upload_v2.call_args
    sent = {k: v for k, v in kwargs.items() if v is not None}
    assert sent == {"content": "hello", "filename": "test.txt"}


def test_files_info_compactable():
    assert get_compactor("files_info") is compact_file_list


def test_files_list_compactable():
    assert get_compactor("files_list") is compact_file_list
