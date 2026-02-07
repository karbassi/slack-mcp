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
    kwargs = {}
    if batch_presence_aware is not None:
        kwargs["batch_presence_aware"] = batch_presence_aware
    if presence_sub is not None:
        kwargs["presence_sub"] = presence_sub
    return await client.api_call("rtm.connect", **kwargs)


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
    kwargs = {}
    if batch_presence_aware is not None:
        kwargs["batch_presence_aware"] = batch_presence_aware
    if include_locale is not None:
        kwargs["include_locale"] = include_locale
    if mpim_aware is not None:
        kwargs["mpim_aware"] = mpim_aware
    if no_latest is not None:
        kwargs["no_latest"] = no_latest
    if no_unreads is not None:
        kwargs["no_unreads"] = no_unreads
    if presence_sub is not None:
        kwargs["presence_sub"] = presence_sub
    if simple_latest is not None:
        kwargs["simple_latest"] = simple_latest
    return await client.api_call("rtm.start", **kwargs)
