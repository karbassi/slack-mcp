from tests.conftest import assert_api_call


async def test_blocks_validate(mcp_client, slack_stub):
    blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": "hi"}}]
    result = await mcp_client.call_tool("blocks_validate", {"blocks": blocks})
    assert result.is_error is False
    assert_api_call(slack_stub.api_call, "blocks.validate", blocks=blocks)
