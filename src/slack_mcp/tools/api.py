from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def api_test(
    error: str | None = None,
    foo: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Check API calling code. Helps test your calling code."""
    kwargs = {}
    if error is not None:
        kwargs["error"] = error
    if foo is not None:
        kwargs["foo"] = foo
    return await client.api_call("api.test", **kwargs)
