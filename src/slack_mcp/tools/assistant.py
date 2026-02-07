from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def assistant_threads_set_status(
    channel_id: str,
    thread_ts: str,
    status: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the status for an AI assistant thread."""
    return await client.api_call(
        "assistant.threads.setStatus",
        channel_id=channel_id,
        thread_ts=thread_ts,
        status=status,
    )


@mcp.tool
async def assistant_threads_set_suggested_prompts(
    channel_id: str,
    thread_ts: str,
    prompts: Optional[list] = None,
    title: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set suggested prompts for an AI assistant thread."""
    kwargs = {"channel_id": channel_id, "thread_ts": thread_ts}
    if prompts is not None:
        kwargs["prompts"] = prompts
    if title is not None:
        kwargs["title"] = title
    return await client.api_call("assistant.threads.setSuggestedPrompts", **kwargs)


@mcp.tool
async def assistant_threads_set_title(
    channel_id: str,
    thread_ts: str,
    title: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the title for an AI assistant thread."""
    return await client.api_call(
        "assistant.threads.setTitle",
        channel_id=channel_id,
        thread_ts=thread_ts,
        title=title,
    )
