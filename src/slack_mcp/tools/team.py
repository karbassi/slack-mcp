from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import LONG_TTL, SHORT_TTL, mcp, slack_client


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
    """Get the access logs for the current team.

    Args:
        before: Return logs from before this Unix timestamp (in seconds).
        count: Number of items to return per page (legacy paging).
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        limit: Maximum number of items to return per page (cursor paging).
        page: Page number of results to return (legacy paging).
        team_id: Encoded team ID to get logs for; required if the token belongs to an org-level app (e.g. ``T0123``).
    """
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
    """Get billable users information for the current team.

    Args:
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        limit: Maximum number of items to return per page.
        team_id: Encoded team ID to get billable info for; required for org-level app tokens (e.g. ``T0123``).
        user: A single user to retrieve billable information for, rather than the whole team (e.g. ``U0123``).
    """
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
    """Disconnect an external organization.

    Args:
        target_team: Encoded team ID of the external organization to disconnect (e.g. ``T0123``).
    """
    return await client.api_call(
        "team.externalTeams.disconnect", target_team=target_team
    )


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
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
    """List external teams and their statuses.

    Args:
        connection_status_filter: Filter results by connection status (e.g. ``CONNECTED``, ``DISCONNECTED``).
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        limit: Maximum number of items to return per page.
        slack_connect_pref_filter: Filter results by Slack Connect preferences (e.g. ``["approved_orgs_only"]``).
        sort_direction: Direction to sort results, ``asc`` or ``desc``.
        sort_field: Field to sort results by (e.g. ``team_name``, ``last_active_timestamp``).
        workspace_filter: Filter results to specific workspaces by encoded team ID (e.g. ``["T0123"]``).
    """
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


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def team_info(
    team: str | None = None,
    domain: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about the current team.

    Args:
        team: Encoded team ID to fetch info for; defaults to the authed user's team (e.g. ``T0123``).
        domain: Workspace domain to look up info by, in place of ``team`` (e.g. ``acme`` for ``acme.slack.com``).
    """
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
    """Get the integration activity logs for the current team.

    Args:
        app_id: Filter logs to this app's events (e.g. ``A0123``).
        change_type: Filter logs by change type (e.g. ``added``, ``removed``, ``enabled``, ``disabled``, ``updated``).
        count: Number of items to return per page.
        page: Page number of results to return.
        service_id: Filter logs to this service's events.
        team_id: Encoded team ID to get logs for; required if the token belongs to an org-level app (e.g. ``T0123``).
        user: Filter logs to events performed by this user (e.g. ``U0123``).
    """
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


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def team_preferences_list(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a list of a workspace's team preferences."""
    return await client.api_call("team.preferences.list")


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def team_profile_get(
    visibility: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Retrieve a team's profile.

    Args:
        visibility: Filter profile fields by visibility; one of ``all``, ``visible``, or ``hidden``.
    """
    return await client.api_call("team.profile.get", visibility=visibility)
