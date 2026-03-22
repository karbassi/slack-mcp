from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def session_test(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Check if session tokens (xoxc/xoxd) are valid.

    Calls client.boot as a health check. Returns ok: true if tokens are valid,
    or a clear error message if they are missing, expired, or invalid.
    """
    if not client.xoxc_token or not client.xoxd_token:
        return {
            "ok": False,
            "error": "missing_tokens",
            "message": "SLACK_XOXC_TOKEN and/or SLACK_XOXD_TOKEN not set.",
        }
    try:
        result = await client.session_call("client.boot")
        if result.get("ok"):
            return {"ok": True, "message": "Session tokens are valid."}
        error = result.get("error", "unknown_error")
        return {
            "ok": False,
            "error": error,
            "message": f"Session tokens may be expired or invalid ({error}). "
            "Re-grab xoxc/xoxd from browser cookies while logged into slack.com.",
        }
    except ValueError as e:
        return {"ok": False, "error": "invalid_or_expired", "message": str(e)}
    except Exception as e:
        return {"ok": False, "error": type(e).__name__, "message": str(e)}


@mcp.tool
async def client_boot(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Boot the Slack client (undocumented session endpoint)."""
    return await client.session_call("client.boot")


@mcp.tool
async def client_counts(
    thread_count_by_last_read: bool | None = None,
    org_wide_aware: bool | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get unread counts and thread info (undocumented session endpoint)."""
    kwargs = {}
    if thread_count_by_last_read is not None:
        kwargs["thread_count_by_last_read"] = thread_count_by_last_read
    if org_wide_aware is not None:
        kwargs["org_wide_aware"] = org_wide_aware
    return await client.session_call("client.counts", **kwargs)


@mcp.tool
async def client_user_boot(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Boot the Slack client for a specific user (undocumented session endpoint)."""
    return await client.session_call("client.userBoot")


@mcp.tool
async def subscriptions_thread_mark(
    channel: str,
    thread_ts: str,
    read: bool = True,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Mark a thread as read or unread (undocumented session endpoint)."""
    return await client.session_call(
        "subscriptions.thread.mark",
        channel=channel,
        thread_ts=thread_ts,
        read=read,
    )


@mcp.tool
async def threads_get_view(
    current_ts: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get thread view data (undocumented session endpoint)."""
    kwargs = {}
    if current_ts is not None:
        kwargs["current_ts"] = current_ts
    return await client.session_call("threads.getView", **kwargs)
