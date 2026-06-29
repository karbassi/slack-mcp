from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def dialog_open(
    dialog: dict[str, str],
    trigger_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Open a dialog with a user.

    Args:
        dialog: Dialog definition for the modal, including ``title``, ``callback_id``, and ``elements``.
        trigger_id: Trigger ID from a user interaction authorizing the dialog; expires after 3 seconds.
    """
    return await client.api_call("dialog.open", dialog=dialog, trigger_id=trigger_id)
