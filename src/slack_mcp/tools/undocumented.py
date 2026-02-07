from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def client_boot(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Boot the Slack client (undocumented session endpoint)."""
    return await client.session_call("client.boot")


@mcp.tool
async def client_counts(
    thread_count_by_last_read: bool | None = None,
    org_wide_aware: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get unread counts and thread info (undocumented session endpoint)."""
    kwargs = {}
    if thread_count_by_last_read is not None:
        kwargs["thread_count_by_last_read"] = thread_count_by_last_read
    if org_wide_aware is not None:
        kwargs["org_wide_aware"] = org_wide_aware
    return await client.session_call("client.counts", **kwargs)


@mcp.tool
async def client_user_boot(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Boot the Slack client for a specific user (undocumented session endpoint)."""
    return await client.session_call("client.userBoot")


@mcp.tool
async def threads_get_view(
    current_ts: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get thread view data (undocumented session endpoint)."""
    kwargs = {}
    if current_ts is not None:
        kwargs["current_ts"] = current_ts
    return await client.session_call("threads.getView", **kwargs)
