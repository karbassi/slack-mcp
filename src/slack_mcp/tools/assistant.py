from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import SLOW_CALL_TIMEOUT, mcp, slack_client


@mcp.tool(timeout=SLOW_CALL_TIMEOUT)
async def assistant_search_context(
    query: str,
    action_token: str | None = None,
    channel_types: str | None = None,
    content_types: str | None = None,
    context_channel_id: str | None = None,
    include_bots: bool | None = None,
    include_context_messages: bool | None = None,
    cursor: str | None = None,
    limit: int | None = None,
    before: int | None = None,
    after: int | None = None,
    sort: str | None = None,
    sort_dir: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search messages, files, channels, and users to provide context to an AI assistant.

    Args:
        query: The search query or user prompt, e.g. ``"What is project gizmo?"``.
        action_token: Required when calling with a bot token; not needed for user tokens.
        channel_types: Comma-separated: ``public_channel``, ``private_channel``, ``mpim``, ``im``.
        content_types: Comma-separated: ``messages``, ``files``, ``channels``, ``users``.
        context_channel_id: Channel to bias results toward.
        include_bots: Include messages from bots in results.
        include_context_messages: Return surrounding messages for each match.
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        limit: Results per page (max 20).
        before: Only results before this UNIX timestamp.
        after: Only results after this UNIX timestamp.
        sort: ``score`` (relevance) or ``timestamp`` (recency).
        sort_dir: Sort direction — ``asc`` or ``desc``.
    """
    return await client.api_call(
        "assistant.search.context",
        query=query,
        action_token=action_token,
        channel_types=channel_types,
        content_types=content_types,
        context_channel_id=context_channel_id,
        include_bots=include_bots,
        include_context_messages=include_context_messages,
        cursor=cursor,
        limit=limit,
        before=before,
        after=after,
        sort=sort,
        sort_dir=sort_dir,
    )


@mcp.tool
async def assistant_search_info(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get search capabilities for the team.

    Returns whether AI/semantic search is available (``is_ai_search_enabled``).
    """
    return await client.api_call("assistant.search.info")


@mcp.tool
async def assistant_threads_set_status(
    channel_id: str,
    thread_ts: str,
    status: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the status for an AI assistant thread.

    Args:
        channel_id: ID of the channel containing the assistant thread (e.g. ``C0123``).
        thread_ts: Timestamp of the parent assistant thread (e.g. ``1700000000.000100``).
        status: Status text to display, e.g. ``"is thinking..."``. Empty string clears the status.
    """
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
    prompts: list[dict[str, str]] | None = None,
    title: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set suggested prompts for an AI assistant thread.

    Args:
        channel_id: ID of the channel containing the assistant thread (e.g. ``C0123``).
        thread_ts: Timestamp of the parent assistant thread (e.g. ``1700000000.000100``).
        prompts: List of prompt objects, each with ``title`` and ``message`` keys.
        title: Optional heading shown above the suggested prompts.
    """
    return await client.api_call(
        "assistant.threads.setSuggestedPrompts",
        channel_id=channel_id,
        thread_ts=thread_ts,
        prompts=prompts,
        title=title,
    )


@mcp.tool
async def assistant_threads_set_title(
    channel_id: str,
    thread_ts: str,
    title: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Set the title for an AI assistant thread.

    Args:
        channel_id: ID of the channel containing the assistant thread (e.g. ``C0123``).
        thread_ts: Timestamp of the parent assistant thread (e.g. ``1700000000.000100``).
        title: Title text to set for the thread.
    """
    return await client.api_call(
        "assistant.threads.setTitle",
        channel_id=channel_id,
        thread_ts=thread_ts,
        title=title,
    )
