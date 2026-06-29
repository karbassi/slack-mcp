from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def rtm_connect(
    batch_presence_aware: bool | None = None,
    presence_sub: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Start a Real Time Messaging session.

    Args:
        batch_presence_aware: Batch presence deliveries, only for users subscribed via ``presence_sub`` events.
        presence_sub: Only deliver presence events for users subscribed via a ``presence_sub`` event.
    """
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
    """Start a Real Time Messaging session (deprecated, use rtm.connect).

    Args:
        batch_presence_aware: Batch presence deliveries, only for users subscribed via ``presence_sub`` events.
        include_locale: Include locale information for users and IMs in the returned data.
        mpim_aware: Return group-DM (multi-party IM) conversations in the returned data.
        no_latest: Exclude latest timestamps for channels, groups, MPIMs, and IMs to reduce payload size.
        no_unreads: Skip unread counts for each channel to reduce payload size.
        presence_sub: Only deliver presence events for users subscribed via a ``presence_sub`` event.
        simple_latest: Return only the latest message timestamp per channel, omitting the full message object.
    """
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
