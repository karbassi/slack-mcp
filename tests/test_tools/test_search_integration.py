import pytest

from slack_mcp.tools.search import (
    enterprise_search_get_connectors,
    search_all,
    search_files,
    search_inline,
    search_messages,
    search_save,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_all_live(live_client):
    result = await search_all(query="test", client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_files_live(live_client):
    result = await search_files(query="test", client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_messages_live(live_client):
    result = await search_messages(query="test", client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.usefixtures("requires_session_tokens")
async def test_search_inline_channel_live(live_client):
    conv = await live_client.session_call(
        "conversations.list", types="public_channel", limit=1
    )
    channels = conv.get("channels", [])
    if not channels:
        pytest.skip("no channels available to scope inline search")
    result = await search_inline(
        query="test", count=5, channel=channels[0]["id"], client=live_client
    )
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.usefixtures("requires_session_tokens")
async def test_search_inline_user_live(live_client):
    boot = await live_client.session_call("client.userBoot")
    uid = boot.get("self", {}).get("id")
    assert uid, "could not resolve own user id"
    result = await search_inline(query="test", count=5, user=uid, client=live_client)
    assert result["ok"] is True


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.usefixtures("requires_session_tokens")
async def test_search_inline_requires_one_scope(live_client):
    result = await search_inline(query="test", client=live_client)
    assert result["ok"] is False


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.usefixtures("requires_session_tokens")
async def test_search_save_live(live_client):
    # WRITE: saves a throwaway search, then removes it via search.delete so the
    # workspace is left clean.
    terms = "slackmcp_integration_test_71"
    try:
        result = await search_save(terms=terms, type="message", client=live_client)
        assert result["ok"] is True
    finally:
        await live_client.session_call_form(
            "search.delete", terms=terms, type="message"
        )


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.usefixtures("requires_session_tokens")
async def test_enterprise_search_get_connectors_live(live_client):
    result = await enterprise_search_get_connectors(client=live_client)
    assert result["ok"] is True
