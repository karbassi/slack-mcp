import json
import uuid

import httpx
from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import compact_items, compact_message_list, compactable
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
    except ValueError as e:
        return {"ok": False, "error": "invalid_or_expired", "message": str(e)}
    except (httpx.HTTPError, OSError, TimeoutError) as e:
        return {"ok": False, "error": type(e).__name__, "message": str(e)}
    else:
        if result.get("ok"):
            return {"ok": True, "message": "Session tokens are valid."}
        error = result.get("error", "unknown_error")
        return {
            "ok": False,
            "error": error,
            "message": f"Session tokens may be expired or invalid ({error}). "
            "Re-grab xoxc/xoxd from browser cookies while logged into slack.com.",
        }


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
    return await client.session_call(
        "client.counts",
        thread_count_by_last_read=thread_count_by_last_read,
        org_wide_aware=org_wide_aware,
    )


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
    return await client.session_call("threads.getView", current_ts=current_ts)


def _pad_draft_ts(ts: str) -> str:
    """Pad a draft timestamp to 7 decimal places (required by Slack)."""
    if "." in ts:
        integer, frac = ts.split(".", 1)
        return f"{integer}.{frac:<07}"
    return ts


def _draft_body(
    channel_id: str,
    text: str,
    thread_ts: str | None = None,
    broadcast: bool = False,
    file_ids: list[str] | None = None,
) -> dict:
    """Build the shared wire payload for drafts.create / drafts.update.

    A draft is plain text wrapped as a Block Kit ``rich_text`` block, addressed
    to a destination (a channel, optionally a thread with ``broadcast``), with
    attached files and a fresh ``client_msg_id``.

    The drafts endpoints expect ``blocks``, ``destinations`` and ``file_ids`` as
    JSON *strings* nested inside the JSON request body (double-encoded) — that
    quirk is centralized here so the two callers can't drift.
    """
    blocks = [
        {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [{"type": "text", "text": text}],
                }
            ],
        }
    ]
    destination: dict = {"channel_id": channel_id}
    if thread_ts is not None:
        destination["thread_ts"] = thread_ts
        destination["broadcast"] = broadcast
    return {
        "blocks": json.dumps(blocks),
        "destinations": json.dumps([destination]),
        "client_msg_id": str(uuid.uuid4()),
        "file_ids": json.dumps(file_ids or []),
    }


# --- Drafts ---


@mcp.tool
async def drafts_list(
    is_active: bool | None = None,
    limit: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List all unsent message drafts (undocumented session endpoint)."""
    kwargs = {}
    if is_active is not None:
        kwargs["is_active"] = str(is_active).lower()
    if limit is not None:
        kwargs["limit"] = str(limit)
    return await client.session_call("drafts.list", **kwargs)


@mcp.tool
async def drafts_create(
    channel_id: str,
    text: str,
    thread_ts: str | None = None,
    broadcast: bool = False,
    file_ids: list[str] | None = None,
    date_scheduled: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Create a message draft (undocumented session endpoint).

    Text is automatically wrapped in Block Kit rich_text format.
    """
    # is_from_composer is sent on create only (matches observed Slack behavior).
    return await client.session_call(
        "drafts.create",
        **_draft_body(channel_id, text, thread_ts, broadcast, file_ids),
        is_from_composer="true",
        date_scheduled=date_scheduled,
    )


@mcp.tool
async def drafts_update(
    draft_id: str,
    client_last_updated_ts: str,
    channel_id: str,
    text: str,
    thread_ts: str | None = None,
    broadcast: bool = False,
    file_ids: list[str] | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update an existing draft (undocumented session endpoint)."""
    return await client.session_call(
        "drafts.update",
        **_draft_body(channel_id, text, thread_ts, broadcast, file_ids),
        draft_id=draft_id,
        client_last_updated_ts=_pad_draft_ts(client_last_updated_ts),
    )


@mcp.tool
async def drafts_delete(
    draft_id: str,
    client_last_updated_ts: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a draft (undocumented session endpoint).

    If client_last_updated_ts is omitted, the latest timestamp is fetched
    automatically from drafts.list to avoid conflict errors.
    """
    if client_last_updated_ts is None:
        drafts = await client.session_call("drafts.list")
        for draft in drafts.get("drafts", []):
            if draft["id"] == draft_id:
                client_last_updated_ts = draft["last_updated_ts"]
                break
        if client_last_updated_ts is None:
            return {"ok": False, "error": "draft_not_found"}
    return await client.session_call_form(
        "drafts.delete",
        draft_id=draft_id,
        client_last_updated_ts=_pad_draft_ts(client_last_updated_ts),
    )


# --- Saved Items ---


@mcp.tool
@compactable(compact_items)
async def saved_list(
    cursor: str | None = None,
    limit: int | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List saved-for-later items. Set detailed=True for full response."""
    return await client.session_call("saved.list", cursor=cursor, limit=limit)


@mcp.tool
async def saved_add(
    item_type: str,
    item_id: str,
    ts: str,
    date_due: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Save a message for later (undocumented session endpoint)."""
    return await client.session_call(
        "saved.add", item_type=item_type, item_id=item_id, ts=ts, date_due=date_due
    )


@mcp.tool
async def saved_delete(
    item_type: str,
    item_id: str,
    ts: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a saved-for-later item (undocumented session endpoint)."""
    return await client.session_call_form(
        "saved.delete", item_type=item_type, item_id=item_id, ts=ts
    )


# --- Emoji (undocumented workspace-level) ---


@mcp.tool
async def emoji_add(
    name: str,
    image_url: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Add a custom emoji from a URL (undocumented session endpoint)."""
    async with httpx.AsyncClient() as http:
        resp = await http.get(image_url)
        resp.raise_for_status()
    content_type = resp.headers.get("content-type", "image/png")
    ext = content_type.split("/")[-1].split(";")[0]
    return await client.session_call_multipart(
        "emoji.add",
        data={"name": name, "mode": "data"},
        files={"image": (f"{name}.{ext}", resp.content, content_type)},
    )


@mcp.tool
async def emoji_remove(
    name: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a custom emoji (undocumented session endpoint)."""
    return await client.session_call_form("emoji.remove", name=name)


@mcp.tool
async def emoji_admin_list(
    page: int | None = None,
    count: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List custom emoji with metadata (undocumented session endpoint)."""
    return await client.session_call("emoji.adminList", page=page, count=count)


# --- Search modules (granular search) ---


@mcp.tool
@compactable(compact_message_list)
async def search_modules_messages(
    query: str,
    cursor: str | None = None,
    count: int | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search messages (undocumented). Set detailed=True for full response."""
    return await client.session_call(
        "search.modules.messages", query=query, cursor=cursor, count=count
    )


@mcp.tool
async def search_modules_files(
    query: str,
    cursor: str | None = None,
    count: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search files (undocumented session endpoint)."""
    return await client.session_call(
        "search.modules.files", query=query, cursor=cursor, count=count
    )


@mcp.tool
async def search_modules_channels(
    query: str,
    cursor: str | None = None,
    count: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search channels by name or topic (undocumented session endpoint)."""
    return await client.session_call(
        "search.modules.channels", query=query, cursor=cursor, count=count
    )


@mcp.tool
async def search_modules_people(
    query: str,
    cursor: str | None = None,
    count: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search people by name, title, or department (undocumented session endpoint)."""
    return await client.session_call(
        "search.modules.people", query=query, cursor=cursor, count=count
    )


@mcp.tool
async def search_modules_dms(
    query: str,
    cursor: str | None = None,
    count: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Search within direct messages only (undocumented session endpoint)."""
    return await client.session_call(
        "search.modules.dms", query=query, cursor=cursor, count=count
    )


# --- Conversations (undocumented extensions) ---


@mcp.tool
@compactable(compact_message_list)
async def conversations_view(
    channel: str,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get channel view with read state. Set detailed=True for full response."""
    return await client.session_call("conversations.view", channel=channel)


@mcp.tool
async def conversations_list_prefs(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get per-channel notification and mute prefs (undocumented)."""
    return await client.session_call("conversations.listPrefs")


# --- Users (undocumented extensions) ---


@mcp.tool
async def users_channel_sections_list(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get sidebar sections and favorites (undocumented session endpoint)."""
    return await client.session_call("users.channelSections.list")


@mcp.tool
async def users_priority_list(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get contacts ranked by interaction frequency (undocumented session endpoint)."""
    return await client.session_call("users.priority.list")


# --- Workspace introspection ---


@mcp.tool
async def experiments_get_by_user(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get A/B experiment assignments for current user (undocumented)."""
    return await client.session_call("experiments.getByUser")


@mcp.tool
async def api_features(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get workspace feature flags (undocumented session endpoint)."""
    return await client.session_call("api.features")


@mcp.tool
async def ai_apps_list(
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List AI apps in the workspace (undocumented session endpoint)."""
    return await client.session_call("aiApps.list")
