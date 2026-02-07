from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def calls_add(
    external_unique_id: str,
    join_url: str,
    created_by: Optional[str] = None,
    date_start: Optional[int] = None,
    desktop_app_join_url: Optional[str] = None,
    external_display_id: Optional[str] = None,
    title: Optional[str] = None,
    users: Optional[list] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Register a new call."""
    kwargs = {"external_unique_id": external_unique_id, "join_url": join_url}
    if created_by is not None:
        kwargs["created_by"] = created_by
    if date_start is not None:
        kwargs["date_start"] = date_start
    if desktop_app_join_url is not None:
        kwargs["desktop_app_join_url"] = desktop_app_join_url
    if external_display_id is not None:
        kwargs["external_display_id"] = external_display_id
    if title is not None:
        kwargs["title"] = title
    if users is not None:
        kwargs["users"] = users
    return await client.api_call("calls.add", **kwargs)


@mcp.tool
async def calls_end(
    id: str,
    duration: Optional[int] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """End a call."""
    kwargs = {"id": id}
    if duration is not None:
        kwargs["duration"] = duration
    return await client.api_call("calls.end", **kwargs)


@mcp.tool
async def calls_info(
    id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about a call."""
    return await client.api_call("calls.info", id=id)


@mcp.tool
async def calls_participants_add(
    id: str,
    users: list,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Register new participants added to a call."""
    return await client.api_call("calls.participants.add", id=id, users=users)


@mcp.tool
async def calls_participants_remove(
    id: str,
    users: list,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Register participants removed from a call."""
    return await client.api_call("calls.participants.remove", id=id, users=users)


@mcp.tool
async def calls_update(
    id: str,
    desktop_app_join_url: Optional[str] = None,
    join_url: Optional[str] = None,
    title: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update information about a call."""
    kwargs = {"id": id}
    if desktop_app_join_url is not None:
        kwargs["desktop_app_join_url"] = desktop_app_join_url
    if join_url is not None:
        kwargs["join_url"] = join_url
    if title is not None:
        kwargs["title"] = title
    return await client.api_call("calls.update", **kwargs)
