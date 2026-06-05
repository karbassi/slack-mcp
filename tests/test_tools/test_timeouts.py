"""Assert that slow paginated read tools carry the 30 s timeout."""

import pytest

from slack_mcp.server import SLOW_CALL_TIMEOUT, mcp


@pytest.mark.asyncio
async def test_slow_read_tools_have_timeout():
    tool_names = [
        "search_all",
        "search_files",
        "search_messages",
        "conversations_history",
        "conversations_replies",
    ]
    for name in tool_names:
        tool = await mcp.get_tool(name)
        assert tool.timeout == SLOW_CALL_TIMEOUT, (
            f"{name}: expected timeout={SLOW_CALL_TIMEOUT}, got {tool.timeout}"
        )
