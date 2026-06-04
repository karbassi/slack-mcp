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
    return await client.api_call(
        "team.accessLogs",
        before=before,
        count=count,
        cursor=cursor,
        limit=limit,
        page=page,
        team_id=team_id,
    )


@mcp.tool
async def team_billable_info(
    cursor: str | None = None,
    limit: int | None = None,
    team_id: str | None = None,
    user: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get billable users information for the current team."""
    return await client.api_call(
        "team.billableInfo",
        cursor=cursor,
        limit=limit,
        team_id=team_id,
        user=user,
    )


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
    return await client.api_call(
        "team.externalTeams.list",
        connection_status_filter=connection_status_filter,
        cursor=cursor,
        limit=limit,
        slack_connect_pref_filter=slack_connect_pref_filter,
        sort_direction=sort_direction,
        sort_field=sort_field,
        workspace_filter=workspace_filter,
    )


@mcp.tool
async def team_info(
    team: str | None = None,
    domain: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about the current team."""
    return await client.api_call("team.info", team=team, domain=domain)


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
    return await client.api_call(
        "team.integrationLogs",
        app_id=app_id,
        change_type=change_type,
        count=count,
        page=page,
        service_id=service_id,
        team_id=team_id,
        user=user,
    )


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
    return await client.api_call("team.profile.get", visibility=visibility)
