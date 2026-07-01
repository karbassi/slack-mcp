from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import (
    compact_search_all,
    compact_search_files,
    compact_search_messages,
    compactable,
)
from slack_mcp.server import SHORT_TTL, SLOW_CALL_TIMEOUT, mcp, slack_client


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


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def search_inline(
    query: str,
    count: int | None = None,
    channel: str | None = None,
    user: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Inline (quick) search scoped to a single channel or user.

    Undocumented session endpoint (``search.inline``) that powers Slack's
    in-context quick-search box. Exactly one of ``channel`` or ``user`` must be
    supplied to scope the search; passing neither or both is rejected by Slack.

    Args:
        query: Search text. Supports Slack modifiers like ``from:@user`` and ``before:2024-01-31``.
        count: Maximum number of results to return.
        channel: Encoded channel ID (e.g. ``C0123ABC``) to scope the search to. Mutually exclusive with ``user``.
        user: Encoded user ID (e.g. ``U0123ABC``) to scope the search to. Mutually exclusive with ``channel``.

    Returns:
        A dict with ``ok``, ``query`` (the parsed query), ``pagination``, and
        ``items`` (the matched messages).
    """
    if (channel is None) == (user is None):
        return {
            "ok": False,
            "error": "invalid_arguments",
            "message": "Provide exactly one of 'channel' or 'user' to scope the search.",
        }
    return await client.session_call_form(
        "search.inline",
        query=query,
        count=count,
        channel=channel,
        user=user,
    )


@mcp.tool
async def search_save(
    terms: str,
    type: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Save a search so it appears in Slack's saved-searches list (WRITE).

    Undocumented session endpoint (``search.save``). This mutates workspace
    state; it is not cached.

    Args:
        terms: The search query string to save (e.g. ``from:@alice deploy``).
        type: The kind of search to save, e.g. ``message`` or ``file``.

    Returns:
        A dict with ``ok`` indicating whether the search was saved.
    """
    return await client.session_call_form(
        "search.save",
        terms=terms,
        type=type,
    )


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def enterprise_search_get_connectors(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List the workspace's enterprise search connectors.

    Undocumented session endpoint (``enterpriseSearch.getConnectors``). Takes no
    arguments.

    Returns:
        A dict with ``ok`` and ``connectors`` (the configured enterprise search connectors).
    """
    return await client.session_call("enterpriseSearch.getConnectors")


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
