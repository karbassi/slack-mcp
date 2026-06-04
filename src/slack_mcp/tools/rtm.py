from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def rtm_connect(
    batch_presence_aware: bool | None = None,
    presence_sub: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Start a Real Time Messaging session."""
    return await client.api_call(
        "rtm.connect",
        batch_presence_aware=batch_presence_aware,
        presence_sub=presence_sub,
    )


@mcp.tool
async def rtm_start(
    batch_presence_aware: bool | None = None,
    include_locale: bool | None = None,
    mpim_aware: bool | None = None,
    no_latest: bool | None = None,
    no_unreads: bool | None = None,
    presence_sub: bool | None = None,
    simple_latest: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Start a Real Time Messaging session (deprecated, use rtm.connect)."""
    return await client.api_call(
        "rtm.start",
        batch_presence_aware=batch_presence_aware,
        include_locale=include_locale,
        mpim_aware=mpim_aware,
        no_latest=no_latest,
        no_unreads=no_unreads,
        presence_sub=presence_sub,
        simple_latest=simple_latest,
    )
