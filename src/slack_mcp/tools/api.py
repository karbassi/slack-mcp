from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool(tags={"skip-resolution"})
async def api_test(
    error: str | None = None,
    foo: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Check API calling code. Helps test your calling code.

    Args:
        error: Error response to return. If set, the call responds with an error of this value.
        foo: Example property to return in the response (echoed back as ``args.foo``).
    """
    return await client.api_call("api.test", error=error, foo=foo)
