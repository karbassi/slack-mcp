from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def team_access_logs(
    before: int | None = None,
    count: int | None = None,
    cursor: str | None = None,
    limit: int | None = None,
    page: int | None = None,
    team_id: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get the access logs for the current team."""
    kwargs = {}
    if before is not None:
        kwargs["before"] = before
    if count is not None:
        kwargs["count"] = count
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit
    if page is not None:
        kwargs["page"] = page
    if team_id is not None:
        kwargs["team_id"] = team_id
    return await client.api_call("team.accessLogs", **kwargs)


@mcp.tool
async def team_billable_info(
    cursor: str | None = None,
    limit: int | None = None,
    team_id: str | None = None,
    user: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get billable users information for the current team."""
    kwargs = {}
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit
    if team_id is not None:
        kwargs["team_id"] = team_id
    if user is not None:
        kwargs["user"] = user
    return await client.api_call("team.billableInfo", **kwargs)


@mcp.tool
async def team_billing_info(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Read a workspace's billing plan information."""
    return await client.api_call("team.billing.info")


@mcp.tool
async def team_external_teams_disconnect(
    target_team: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Disconnect an external organization."""
    return await client.api_call(
        "team.externalTeams.disconnect", target_team=target_team
    )


@mcp.tool
async def team_external_teams_list(
    connection_status_filter: str | None = None,
    cursor: str | None = None,
    limit: int | None = None,
    slack_connect_pref_filter: list | None = None,
    sort_direction: str | None = None,
    sort_field: str | None = None,
    workspace_filter: list | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List external teams and their statuses."""
    kwargs = {}
    if connection_status_filter is not None:
        kwargs["connection_status_filter"] = connection_status_filter
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit
    if slack_connect_pref_filter is not None:
        kwargs["slack_connect_pref_filter"] = slack_connect_pref_filter
    if sort_direction is not None:
        kwargs["sort_direction"] = sort_direction
    if sort_field is not None:
        kwargs["sort_field"] = sort_field
    if workspace_filter is not None:
        kwargs["workspace_filter"] = workspace_filter
    return await client.api_call("team.externalTeams.list", **kwargs)


@mcp.tool
async def team_info(
    team: str | None = None,
    domain: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about the current team."""
    kwargs = {}
    if team is not None:
        kwargs["team"] = team
    if domain is not None:
        kwargs["domain"] = domain
    return await client.api_call("team.info", **kwargs)


@mcp.tool
async def team_integration_logs(
    app_id: str | None = None,
    change_type: str | None = None,
    count: int | None = None,
    page: int | None = None,
    service_id: str | None = None,
    team_id: str | None = None,
    user: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get the integration activity logs for the current team."""
    kwargs = {}
    if app_id is not None:
        kwargs["app_id"] = app_id
    if change_type is not None:
        kwargs["change_type"] = change_type
    if count is not None:
        kwargs["count"] = count
    if page is not None:
        kwargs["page"] = page
    if service_id is not None:
        kwargs["service_id"] = service_id
    if team_id is not None:
        kwargs["team_id"] = team_id
    if user is not None:
        kwargs["user"] = user
    return await client.api_call("team.integrationLogs", **kwargs)


@mcp.tool
async def team_preferences_list(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a list of a workspace's team preferences."""
    return await client.api_call("team.preferences.list")


@mcp.tool
async def team_profile_get(
    visibility: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a team's profile."""
    kwargs = {}
    if visibility is not None:
        kwargs["visibility"] = visibility
    return await client.api_call("team.profile.get", **kwargs)
