import json
import uuid
from typing import Any

import httpx
from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import (
    compact_items,
    compact_message_list,
    compact_messages_by_channel,
    compactable,
)
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
    """Get unread counts and thread info (undocumented session endpoint).

    Args:
        thread_count_by_last_read: Count unread threads relative to the last-read marker.
        org_wide_aware: Include counts across all workspaces in an Enterprise org.
    """
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
    """Mark a thread as read or unread (undocumented session endpoint).

    Args:
        channel: ID of the channel containing the thread (e.g. ``C0123``).
        thread_ts: Timestamp of the parent thread message (e.g. ``1700000000.000100``).
        read: Mark the thread as read (``True``) or unread (``False``).
    """
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
    """Get thread view data (undocumented session endpoint).

    Args:
        current_ts: Timestamp anchoring the thread view to page from (e.g. ``1700000000.000100``).
    """
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
    """List all unsent message drafts (undocumented session endpoint).

    Args:
        is_active: Only return drafts that are currently active (unsent).
        limit: Maximum number of drafts to return.
    """
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

    Args:
        channel_id: ID of the channel the draft is addressed to (e.g. ``C0123``).
        text: Draft message body text.
        thread_ts: Timestamp of the parent thread to draft a reply to (e.g. ``1700000000.000100``).
        broadcast: Also send the threaded reply to the channel when posted (requires ``thread_ts``).
        file_ids: IDs of already-uploaded files to attach to the draft (e.g. ``F0123``).
        date_scheduled: Unix epoch timestamp (seconds) to schedule the draft for sending.
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
    """Update an existing draft (undocumented session endpoint).

    Args:
        draft_id: ID of the draft to update.
        client_last_updated_ts: The draft's last-updated timestamp (7-decimal-place Slack draft ts).
        channel_id: ID of the channel the draft is addressed to (e.g. ``C0123``).
        text: Updated draft message body text.
        thread_ts: Timestamp of the parent thread to draft a reply to (e.g. ``1700000000.000100``).
        broadcast: Also send the threaded reply to the channel when posted (requires ``thread_ts``).
        file_ids: IDs of already-uploaded files to attach to the draft (e.g. ``F0123``).
    """
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

    Args:
        draft_id: ID of the draft to delete.
        client_last_updated_ts: The draft's last-updated timestamp (7-decimal-place Slack draft ts).
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
    """List saved-for-later items. Set detailed=True for full response.

    Args:
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        limit: Maximum number of saved items to return.
        detailed: Return the full, uncompacted response instead of the compacted summary.
    """
    return await client.session_call("saved.list", cursor=cursor, limit=limit)


@mcp.tool
async def saved_add(
    item_type: str,
    item_id: str,
    ts: str,
    date_due: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Save a message for later (undocumented session endpoint).

    Args:
        item_type: Type of item to save, e.g. ``message``.
        item_id: ID of the item's container, e.g. the channel ID for a message (``C0123``).
        ts: Timestamp of the item to save (e.g. ``1700000000.000100``).
        date_due: Unix epoch timestamp (seconds) for an optional reminder/due date.
    """
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
    """Remove a saved-for-later item (undocumented session endpoint).

    Args:
        item_type: Type of saved item to remove, e.g. ``message``.
        item_id: ID of the item's container, e.g. the channel ID for a message (``C0123``).
        ts: Timestamp of the saved item to remove (e.g. ``1700000000.000100``).
    """
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
    """Add a custom emoji from a URL (undocumented session endpoint).

    Args:
        name: Name for the new emoji, without colons (e.g. ``party_parrot``).
        image_url: URL of the image to download and upload as the emoji.
    """
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
    """Remove a custom emoji (undocumented session endpoint).

    Args:
        name: Name of the emoji to remove, without colons (e.g. ``party_parrot``).
    """
    return await client.session_call_form("emoji.remove", name=name)


@mcp.tool
async def emoji_admin_list(
    page: int | None = None,
    count: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List custom emoji with metadata (undocumented session endpoint).

    Args:
        page: 1-based page number of results to return.
        count: Number of emoji to return per page.
    """
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
    """Search messages (undocumented). Set detailed=True for full response.

    Args:
        query: Search query string, supporting Slack search operators (e.g. ``from:@user``).
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        count: Number of results to return per page.
        detailed: Return the full, uncompacted response instead of the compacted summary.
    """
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
    """Search files (undocumented session endpoint).

    Args:
        query: Search query string matching file names and contents.
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        count: Number of results to return per page.
    """
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
    """Search channels by name or topic (undocumented session endpoint).

    Args:
        query: Search query string matching channel names and topics.
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        count: Number of results to return per page.
    """
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
    """Search people by name, title, or department (undocumented session endpoint).

    Args:
        query: Search query string matching member names, titles, and departments.
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        count: Number of results to return per page.
    """
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
    """Search within direct messages only (undocumented session endpoint).

    Args:
        query: Search query string matched against direct-message content.
        cursor: Pagination cursor from a previous response's ``response_metadata.next_cursor``.
        count: Number of results to return per page.
    """
    return await client.session_call(
        "search.modules.dms", query=query, cursor=cursor, count=count
    )


# --- Messages (batch fetch) ---


@mcp.tool
@compactable(compact_messages_by_channel)
async def messages_list(
    message_ids: list[dict[str, Any]],
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Batch-fetch full message objects by channel and timestamp (undocumented session endpoint).

    Resolves both top-level messages and thread replies in one call — useful for
    hydrating saved/bookmarked items without one ``conversations.history`` call each.
    Set detailed=True for the full, uncompacted response.

    Args:
        message_ids: Groups of messages to fetch, each
            ``{"channel": "C0123", "timestamps": ["1700000000.000100", ...]}``.
        detailed: Return the full, uncompacted response instead of the compacted summary.
    """
    return await client.session_call("messages.list", message_ids=message_ids)


# --- Conversations (undocumented extensions) ---


@mcp.tool
@compactable(compact_message_list)
async def conversations_view(
    channel: str,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get channel view with read state. Set detailed=True for full response.

    Args:
        channel: ID of the channel to view (e.g. ``C0123``).
        detailed: Return the full, uncompacted response instead of the compacted summary.
    """
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
