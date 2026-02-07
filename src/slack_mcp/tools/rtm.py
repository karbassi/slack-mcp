from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def rtm_connect(
    batch_presence_aware: Optional[bool] = None,
    presence_sub: Optional[bool] = None,
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
    batch_presence_aware: Optional[bool] = None,
    include_locale: Optional[bool] = None,
    mpim_aware: Optional[bool] = None,
    no_latest: Optional[bool] = None,
    no_unreads: Optional[bool] = None,
    presence_sub: Optional[bool] = None,
    simple_latest: Optional[bool] = None,
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
