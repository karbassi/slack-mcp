"""Compact response helpers — allowlist-based stripping of Slack API bloat."""

from __future__ import annotations

from collections.abc import Callable  # noqa: TC003
from typing import Any

# -- Decorator + registry --

_COMPACTORS: dict[str, Callable] = {}


def compactable(compactor: Callable):
    """Mark a tool for automatic response compaction."""

    def decorator(fn):
        _COMPACTORS[fn.__name__] = compactor
        return fn

    return decorator


def get_compactor(tool_name: str) -> Callable | None:
    return _COMPACTORS.get(tool_name)


# -- Allowlists --

MESSAGE_FIELDS = frozenset({
    "ts", "user", "username", "text", "type", "subtype", "thread_ts",
    "reply_count", "reply_users_count", "reactions", "permalink",
    "bot_id", "files", "channel",
})

FILE_FIELDS = frozenset({
    "id", "name", "title", "filetype", "mimetype", "size", "user",
    "created", "url_private", "url_private_download", "permalink",
    "external_url", "channels", "mode", "is_external",
})

CHANNEL_FIELDS = frozenset({
    "id", "name", "is_channel", "is_group", "is_im", "is_mpim",
    "is_private", "is_archived", "is_member", "num_members", "topic",
    "purpose", "created", "creator", "updated",
})

CHANNEL_REF_FIELDS = frozenset({
    "id", "name", "is_im", "is_mpim", "is_private", "is_channel",
})

# A reaction keeps its name and tally; the per-user ID array is dropped.
REACTION_FIELDS = frozenset({"name", "count"})

# topic/purpose collapse to just their text; creator/last_set are dropped.
TOPIC_FIELDS = frozenset({"value"})

USER_FIELDS = frozenset({
    "id", "name", "real_name", "team_id", "deleted", "is_bot", "is_app_user",
    "is_admin", "is_owner", "is_primary_owner", "is_restricted",
    "is_ultra_restricted", "is_email_confirmed", "tz", "tz_label", "profile",
})

# One canonical avatar (image_512) survives; the other 8 sizes are dropped.
PROFILE_FIELDS = frozenset({
    "real_name", "display_name", "email", "title", "phone", "pronouns",
    "first_name", "last_name", "status_text", "status_emoji",
    "status_expiration", "image_512",
})


# -- Low-level strippers (mutate in-place) --

def _strip_to(obj: dict, allowed: frozenset[str]) -> None:
    for key in list(obj.keys()):
        if key not in allowed:
            del obj[key]


def strip_message(msg: dict) -> None:
    _strip_to(msg, MESSAGE_FIELDS)
    files = msg.get("files", [])
    if not isinstance(files, list):
        files = []
    for f in files:
        if isinstance(f, dict):
            strip_file(f)
    reactions = msg.get("reactions", [])
    if not isinstance(reactions, list):
        reactions = []
    for r in reactions:
        if isinstance(r, dict):
            _strip_to(r, REACTION_FIELDS)


def strip_file(f: dict) -> None:
    _strip_to(f, FILE_FIELDS)


def strip_channel(ch: dict) -> None:
    _strip_to(ch, CHANNEL_FIELDS)
    for field in ("topic", "purpose"):
        sub = ch.get(field)
        if isinstance(sub, dict):
            _strip_to(sub, TOPIC_FIELDS)


def strip_channel_ref(ch: dict) -> None:
    _strip_to(ch, CHANNEL_REF_FIELDS)


def strip_user(u: dict) -> None:
    _strip_to(u, USER_FIELDS)
    profile = u.get("profile")
    if isinstance(profile, dict):
        strip_profile(profile)


def strip_profile(p: dict) -> None:
    _strip_to(p, PROFILE_FIELDS)


# -- Response-level compactors (mutate in-place) --

def compact_message_list(data: dict[str, Any]) -> None:
    """conversations.history/replies, conversations.view, search.modules.messages."""
    if not data.get("ok"):
        return
    for msg in data.get("messages", []):
        strip_message(msg)


def compact_messages_by_channel(data: dict[str, Any]) -> None:
    """messages.list — messages keyed by channel id."""
    if not data.get("ok"):
        return
    messages = data.get("messages")
    if not isinstance(messages, dict):
        return
    for msgs in messages.values():
        if isinstance(msgs, list):
            for msg in msgs:
                if isinstance(msg, dict):
                    strip_message(msg)


def compact_search_messages(data: dict[str, Any]) -> None:
    """search.messages"""
    if not data.get("ok"):
        return
    messages = data.get("messages")
    if not isinstance(messages, dict):
        return
    matches = messages.get("matches", [])
    if not isinstance(matches, list):
        return
    for msg in matches:
        if not isinstance(msg, dict):
            continue
        strip_message(msg)
        ch = msg.get("channel")
        if isinstance(ch, dict):
            strip_channel_ref(ch)


def compact_search_files(data: dict[str, Any]) -> None:
    """search.files"""
    if not data.get("ok"):
        return
    files = data.get("files")
    if not isinstance(files, dict):
        return
    matches = files.get("matches", [])
    if not isinstance(matches, list):
        return
    for f in matches:
        if isinstance(f, dict):
            strip_file(f)


def compact_search_all(data: dict[str, Any]) -> None:
    """search.all — delegates to both."""
    if not data.get("ok"):
        return
    compact_search_messages(data)
    compact_search_files(data)


def compact_channel_list(data: dict[str, Any]) -> None:
    """conversations.list"""
    if not data.get("ok"):
        return
    channels = data.get("channels", [])
    if not isinstance(channels, list):
        return
    for ch in channels:
        if isinstance(ch, dict):
            strip_channel(ch)


def compact_file_list(data: dict[str, Any]) -> None:
    """files.list (list of files) and files.info (single file)."""
    if not data.get("ok"):
        return
    # files.list shape: {"files": [...]}
    files = data.get("files")
    for f in files if isinstance(files, list) else []:
        if isinstance(f, dict):
            strip_file(f)
    # files.info shape: {"file": {...}}
    single = data.get("file")
    if isinstance(single, dict):
        strip_file(single)


def compact_single_item(data: dict[str, Any]) -> None:
    """reactions.get — single message or file at top level."""
    if not data.get("ok"):
        return
    msg = data.get("message")
    if isinstance(msg, dict):
        strip_message(msg)
    f = data.get("file")
    if isinstance(f, dict):
        strip_file(f)


def compact_users(data: dict[str, Any]) -> None:
    """users.lookupByEmail / users.info (single user), users.list (members),
    users.profile.get (bare profile)."""
    if not data.get("ok"):
        return
    user = data.get("user")
    if isinstance(user, dict):
        strip_user(user)
    members = data.get("members")
    for m in members if isinstance(members, list) else []:
        if isinstance(m, dict):
            strip_user(m)
    profile = data.get("profile")
    if isinstance(profile, dict):
        strip_profile(profile)


def compact_items(data: dict[str, Any]) -> None:
    """reactions/pins/stars/saved — items with nested messages/files."""
    if not data.get("ok"):
        return
    items = data.get("items", [])
    if not isinstance(items, list):
        return
    for item in items:
        if not isinstance(item, dict):
            continue
        msg = item.get("message")
        if isinstance(msg, dict):
            strip_message(msg)
        f = item.get("file")
        if isinstance(f, dict):
            strip_file(f)
