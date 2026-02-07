import pytest
from slack_mcp.tools.undocumented import (
    client_boot,
    client_counts,
    client_user_boot,
    threads_get_view,
)


@pytest.mark.asyncio
async def test_client_boot(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await client_boot(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("client.boot")


@pytest.mark.asyncio
async def test_client_counts(mock_client):
    mock_client.session_call.return_value = {"ok": True, "channels": []}
    result = await client_counts(thread_count_by_last_read=True, client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with(
        "client.counts", thread_count_by_last_read=True
    )


@pytest.mark.asyncio
async def test_client_user_boot(mock_client):
    mock_client.session_call.return_value = {"ok": True}
    result = await client_user_boot(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("client.userBoot")


@pytest.mark.asyncio
async def test_threads_get_view(mock_client):
    mock_client.session_call.return_value = {"ok": True, "threads": []}
    result = await threads_get_view(client=mock_client)
    assert result["ok"] is True
    mock_client.session_call.assert_called_once_with("threads.getView")
