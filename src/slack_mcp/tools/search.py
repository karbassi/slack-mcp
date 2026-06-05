from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import (
    compact_search_all,
    compact_search_files,
    compact_search_messages,
    compactable,
)
from slack_mcp.server import SLOW_CALL_TIMEOUT, mcp, slack_client


@mcp.tool(timeout=SLOW_CALL_TIMEOUT)
@compactable(compact_search_all)
async def search_all(
    query: str,
    count: int | None = None,
    highlight: bool | None = None,
    page: int | None = None,
    sort: str | None = None,
    sort_dir: str | None = None,
    team_id: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search for messages and files.

    Args:
        query: Search text. Supports Slack modifiers like ``in:#channel``, ``from:@user``, and ``before:2024-01-31``.
        count: Results per page (default 20, max 100).
        highlight: Wrap matched terms in highlight markers in the response.
        page: 1-based page number to return.
        sort: Sort by ``score`` (relevance, default) or ``timestamp`` (recency).
        sort_dir: Sort direction, ``asc`` or ``desc`` (default ``desc``).
        team_id: Encoded team ID to scope the search to (for org-wide tokens).
        detailed: Return the full, uncompacted Slack response when True.
    """
    return await client.api_call(
        "search.all",
        query=query,
        count=count,
        highlight=highlight,
        page=page,
        sort=sort,
        sort_dir=sort_dir,
        team_id=team_id,
    )


@mcp.tool(timeout=SLOW_CALL_TIMEOUT)
@compactable(compact_search_files)
async def search_files(
    query: str,
    count: int | None = None,
    highlight: bool | None = None,
    page: int | None = None,
    sort: str | None = None,
    sort_dir: str | None = None,
    team_id: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search for files matching a query.

    Args:
        query: Search text. Supports Slack modifiers like ``in:#channel``, ``from:@user``, and ``type:`` filters.
        count: Results per page (default 20, max 100).
        highlight: Wrap matched terms in highlight markers in the response.
        page: 1-based page number to return.
        sort: Sort by ``score`` (relevance, default) or ``timestamp`` (recency).
        sort_dir: Sort direction, ``asc`` or ``desc`` (default ``desc``).
        team_id: Encoded team ID to scope the search to (for org-wide tokens).
        detailed: Return the full, uncompacted Slack response when True.
    """
    return await client.api_call(
        "search.files",
        query=query,
        count=count,
        highlight=highlight,
        page=page,
        sort=sort,
        sort_dir=sort_dir,
        team_id=team_id,
    )


@mcp.tool(timeout=SLOW_CALL_TIMEOUT)
@compactable(compact_search_messages)
async def search_messages(
    query: str,
    count: int | None = None,
    cursor: str | None = None,
    highlight: bool | None = None,
    page: int | None = None,
    sort: str | None = None,
    sort_dir: str | None = None,
    team_id: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search for messages matching a query.

    Args:
        query: Search text. Supports Slack modifiers like ``in:#channel``, ``from:@user``, and ``before:2024-01-31``.
        count: Results per page (default 20, max 100).
        cursor: Pagination cursor from ``response_metadata.next_cursor`` in a prior response (alternative to ``page``).
        highlight: Wrap matched terms in highlight markers in the response.
        page: 1-based page number to return.
        sort: Sort by ``score`` (relevance, default) or ``timestamp`` (recency).
        sort_dir: Sort direction, ``asc`` or ``desc`` (default ``desc``).
        team_id: Encoded team ID to scope the search to (for org-wide tokens).
        detailed: Return the full, uncompacted Slack response when True.
    """
    return await client.api_call(
        "search.messages",
        query=query,
        count=count,
        cursor=cursor,
        highlight=highlight,
        page=page,
        sort=sort,
        sort_dir=sort_dir,
        team_id=team_id,
    )
