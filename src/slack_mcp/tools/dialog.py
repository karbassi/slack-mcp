from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def dialog_open(
    dialog: dict,
    trigger_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Open a dialog with a user."""
    return await client.api_call(
        "dialog.open", dialog=dialog, trigger_id=trigger_id
    )
