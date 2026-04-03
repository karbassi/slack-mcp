"""Compact response helpers — allowlist-based stripping of Slack API bloat."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

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


def strip_file(f: dict) -> None:
    _strip_to(f, FILE_FIELDS)


def strip_channel(ch: dict) -> None:
    _strip_to(ch, CHANNEL_FIELDS)


def strip_channel_ref(ch: dict) -> None:
    _strip_to(ch, CHANNEL_REF_FIELDS)


# -- Response-level compactors (mutate in-place) --

def compact_message_list(data: dict[str, Any]) -> None:
    """conversations.history/replies, conversations.view, search.modules.messages."""
    if not data.get("ok"):
        return
    for msg in data.get("messages", []):
        strip_message(msg)


def compact_search_messages(data: dict[str, Any]) -> None:
    """search.messages"""
    if not data.get("ok"):
        return
    messages = data.get("messages")
    if not isinstance(messages, dict):
        return
    for msg in messages.get("matches", []):
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
    for f in files.get("matches", []):
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
    for ch in data.get("channels", []):
        strip_channel(ch)


def compact_file_list(data: dict[str, Any]) -> None:
    """files.list (list of files) and files.info (single file)."""
    if not data.get("ok"):
        return
    # files.list shape: {"files": [...]}
    for f in data.get("files", []):
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
