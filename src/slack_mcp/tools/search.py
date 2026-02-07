from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def search_all(
    query: str,
    count: int | None = None,
    highlight: bool | None = None,
    page: int | None = None,
    sort: str | None = None,
    sort_dir: str | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search for messages and files matching a query."""
    kwargs = {"query": query}
    if count is not None:
        kwargs["count"] = count
    if highlight is not None:
        kwargs["highlight"] = highlight
    if page is not None:
        kwargs["page"] = page
    if sort is not None:
        kwargs["sort"] = sort
    if sort_dir is not None:
        kwargs["sort_dir"] = sort_dir
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("search.all", **kwargs)


@mcp.tool
async def search_files(
    query: str,
    count: int | None = None,
    highlight: bool | None = None,
    page: int | None = None,
    sort: str | None = None,
    sort_dir: str | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search for files matching a query."""
    kwargs = {"query": query}
    if count is not None:
        kwargs["count"] = count
    if highlight is not None:
        kwargs["highlight"] = highlight
    if page is not None:
        kwargs["page"] = page
    if sort is not None:
        kwargs["sort"] = sort
    if sort_dir is not None:
        kwargs["sort_dir"] = sort_dir
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("search.files", **kwargs)


@mcp.tool
async def search_messages(
    query: str,
    count: int | None = None,
    cursor: str | None = None,
    highlight: bool | None = None,
    page: int | None = None,
    sort: str | None = None,
    sort_dir: str | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search for messages matching a query."""
    kwargs = {"query": query}
    if count is not None:
        kwargs["count"] = count
    if cursor is not None:
        kwargs["cursor"] = cursor
    if highlight is not None:
        kwargs["highlight"] = highlight
    if page is not None:
        kwargs["page"] = page
    if sort is not None:
        kwargs["sort"] = sort
    if sort_dir is not None:
        kwargs["sort_dir"] = sort_dir
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("search.messages", **kwargs)
