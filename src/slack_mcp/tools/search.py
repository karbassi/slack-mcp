from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def search_all(
    query: str,
    count: Optional[int] = None,
    highlight: Optional[bool] = None,
    page: Optional[int] = None,
    sort: Optional[str] = None,
    sort_dir: Optional[str] = None,
    team_id: Optional[str] = None,
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
    count: Optional[int] = None,
    highlight: Optional[bool] = None,
    page: Optional[int] = None,
    sort: Optional[str] = None,
    sort_dir: Optional[str] = None,
    team_id: Optional[str] = None,
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
    count: Optional[int] = None,
    cursor: Optional[str] = None,
    highlight: Optional[bool] = None,
    page: Optional[int] = None,
    sort: Optional[str] = None,
    sort_dir: Optional[str] = None,
    team_id: Optional[str] = None,
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
