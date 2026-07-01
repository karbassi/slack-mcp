from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import LONG_TTL, mcp, slack_client


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def emoji_list(
    include_categories: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List custom emoji for a team.

    Args:
        include_categories: Include the standard emoji categories in the response when ``True``.
    """
    return await client.api_call("emoji.list", include_categories=include_categories)


@mcp.tool(meta={"cache_ttl": LONG_TTL})
async def emoji_collections_list(
    installed_only: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List emoji collections (packs) available to and installed in the team.

    Uses the undocumented ``emoji.collections.list`` session endpoint.

    Args:
        installed_only: When ``True``, restrict the response to collections the
            team has already installed, omitting the catalog of available packs.

    Returns:
        A dict with:
            installed: Emoji collections the team has installed.
            available: Emoji collections available to install (empty when
                ``installed_only`` is ``True``).
    """
    return await client.session_call(
        "emoji.collections.list", installed_only=installed_only
    )
