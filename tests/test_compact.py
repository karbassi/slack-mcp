"""Tests for compact.py — stripping helpers and compactor functions."""

import copy

# -- Fixtures: representative Slack API payloads --

def _bloated_message():
    return {
        "ts": "1234567890.123456",
        "user": "U123",
        "username": "alice",
        "text": "hello world",
        "type": "message",
        "subtype": None,
        "thread_ts": "1234567890.000000",
        "reply_count": 3,
        "reply_users_count": 2,
        "reactions": [{"name": "thumbsup", "count": 1}],
        "permalink": "https://slack.com/archives/C123/p123",
        "bot_id": None,
        "files": [
            {
                "id": "F1",
                "name": "doc.pdf",
                "title": "Doc",
                "filetype": "pdf",
                "mimetype": "application/pdf",
                "size": 1024,
                "user": "U123",
                "created": 1700000000,
                "url_private": "https://files.slack.com/priv",
                "url_private_download": "https://files.slack.com/dl",
                "permalink": "https://slack.com/files/F1",
                "external_url": None,
                "channels": ["C123"],
                "mode": "hosted",
                "is_external": False,
                # bloat:
                "thumb_64": "https://thumb64",
                "thumb_80": "https://thumb80",
                "thumb_360": "https://thumb360",
            }
        ],
        # bloat fields:
        "blocks": [{"type": "rich_text"}],
        "attachments": [{"fallback": "x"}],
        "client_msg_id": "uuid",
        "team": "T123",
    }


def _bloated_file():
    return {
        "id": "F1",
        "name": "doc.pdf",
        "title": "Doc",
        "filetype": "pdf",
        "mimetype": "application/pdf",
        "size": 1024,
        "user": "U123",
        "created": 1700000000,
        "url_private": "https://files.slack.com/priv",
        "url_private_download": "https://files.slack.com/dl",
        "permalink": "https://slack.com/files/F1",
        "external_url": None,
        "channels": ["C123"],
        "mode": "hosted",
        "is_external": False,
        # bloat:
        "thumb_64": "https://thumb64",
        "thumb_80": "https://thumb80",
        "thumb_360": "https://thumb360",
        "thumb_480": "https://thumb480",
        "original_w": 800,
        "original_h": 600,
    }


def _bloated_channel():
    return {
        "id": "C123",
        "name": "general",
        "is_channel": True,
        "is_group": False,
        "is_im": False,
        "is_mpim": False,
        "is_private": False,
        "is_archived": False,
        "is_member": True,
        "num_members": 42,
        "topic": {"value": "General chat"},
        "purpose": {"value": "A place for everything"},
        "created": 1600000000,
        "creator": "U001",
        "updated": 1700000000,
        # bloat:
        "name_normalized": "general",
        "is_org_shared": False,
        "is_ext_shared": False,
        "is_pending_ext_shared": False,
        "previous_names": ["old-general"],
        "shared_team_ids": ["T123"],
    }


def _bloated_channel_ref():
    return {
        "id": "C123",
        "name": "general",
        "is_im": False,
        "is_mpim": False,
        "is_private": False,
        "is_channel": True,
        # bloat:
        "is_org_shared": False,
        "is_ext_shared": False,
        "name_normalized": "general",
    }


# -- strip_message --

class TestStripMessage:
    def test_keeps_allowed_fields(self):
        from slack_mcp.compact import strip_message
        msg = _bloated_message()
        strip_message(msg)
        assert "ts" in msg
        assert "user" in msg
        assert "text" in msg
        assert "permalink" in msg
        assert "reactions" in msg
        assert "files" in msg

    def test_removes_bloat_fields(self):
        from slack_mcp.compact import strip_message
        msg = _bloated_message()
        strip_message(msg)
        assert "blocks" not in msg
        assert "attachments" not in msg
        assert "client_msg_id" not in msg
        assert "team" not in msg

    def test_strips_nested_files(self):
        from slack_mcp.compact import strip_message
        msg = _bloated_message()
        strip_message(msg)
        f = msg["files"][0]
        assert "id" in f
        assert "name" in f
        assert "thumb_64" not in f
        assert "thumb_80" not in f

    def test_no_files_key_ok(self):
        from slack_mcp.compact import strip_message
        msg = {"ts": "123", "text": "hi", "blocks": []}
        strip_message(msg)
        assert "blocks" not in msg
        assert "ts" in msg

    def test_files_none_does_not_crash(self):
        from slack_mcp.compact import strip_message
        msg = {"ts": "123", "text": "hi", "files": None}
        strip_message(msg)
        assert "ts" in msg

    def test_files_with_non_dict_elements(self):
        from slack_mcp.compact import strip_message
        msg = {"ts": "123", "text": "hi", "files": ["not_a_dict", None, 42]}
        strip_message(msg)
        assert "ts" in msg


# -- strip_file --

class TestStripFile:
    def test_keeps_allowed_fields(self):
        from slack_mcp.compact import strip_file
        f = _bloated_file()
        strip_file(f)
        assert "id" in f
        assert "name" in f
        assert "url_private" in f
        assert "permalink" in f

    def test_removes_thumbnails(self):
        from slack_mcp.compact import strip_file
        f = _bloated_file()
        strip_file(f)
        assert "thumb_64" not in f
        assert "thumb_80" not in f
        assert "thumb_360" not in f
        assert "original_w" not in f


# -- strip_channel --

class TestStripChannel:
    def test_keeps_allowed_fields(self):
        from slack_mcp.compact import strip_channel
        ch = _bloated_channel()
        strip_channel(ch)
        assert "id" in ch
        assert "name" in ch
        assert "num_members" in ch
        assert "topic" in ch

    def test_removes_bloat(self):
        from slack_mcp.compact import strip_channel
        ch = _bloated_channel()
        strip_channel(ch)
        assert "name_normalized" not in ch
        assert "is_org_shared" not in ch
        assert "previous_names" not in ch


# -- strip_channel_ref --

class TestStripChannelRef:
    def test_keeps_allowed_fields(self):
        from slack_mcp.compact import strip_channel_ref
        ch = _bloated_channel_ref()
        strip_channel_ref(ch)
        assert "id" in ch
        assert "name" in ch
        assert "is_channel" in ch

    def test_removes_bloat(self):
        from slack_mcp.compact import strip_channel_ref
        ch = _bloated_channel_ref()
        strip_channel_ref(ch)
        assert "is_org_shared" not in ch
        assert "name_normalized" not in ch


# -- compact_message_list --

class TestCompactMessageList:
    def test_strips_messages(self):
        from slack_mcp.compact import compact_message_list
        data = {
            "ok": True,
            "messages": [_bloated_message(), _bloated_message()],
        }
        compact_message_list(data)
        for msg in data["messages"]:
            assert "blocks" not in msg
            assert "ts" in msg

    def test_passthrough_on_not_ok(self):
        from slack_mcp.compact import compact_message_list
        data = {"ok": False, "error": "channel_not_found"}
        original = copy.deepcopy(data)
        compact_message_list(data)
        assert data == original

    def test_missing_messages_key(self):
        from slack_mcp.compact import compact_message_list
        data = {"ok": True}
        compact_message_list(data)  # should not raise


# -- compact_search_messages --

class TestCompactSearchMessages:
    def test_strips_matches(self):
        from slack_mcp.compact import compact_search_messages
        msg = _bloated_message()
        msg["channel"] = _bloated_channel_ref()
        data = {
            "ok": True,
            "messages": {
                "total": 1,
                "paging": {"count": 20, "total": 1, "page": 1, "pages": 1},
                "matches": [msg],
            },
        }
        compact_search_messages(data)
        m = data["messages"]["matches"][0]
        assert "blocks" not in m
        assert "ts" in m
        ch = m["channel"]
        assert "name_normalized" not in ch

    def test_passthrough_on_not_ok(self):
        from slack_mcp.compact import compact_search_messages
        data = {"ok": False, "error": "invalid_auth"}
        original = copy.deepcopy(data)
        compact_search_messages(data)
        assert data == original

    def test_non_dict_matches_do_not_crash(self):
        from slack_mcp.compact import compact_search_messages
        data = {
            "ok": True,
            "messages": {"matches": ["not_a_dict", None, 42]},
        }
        compact_search_messages(data)


# -- compact_search_files --

class TestCompactSearchFiles:
    def test_strips_file_matches(self):
        from slack_mcp.compact import compact_search_files
        data = {
            "ok": True,
            "files": {
                "total": 1,
                "paging": {"count": 20, "total": 1, "page": 1, "pages": 1},
                "matches": [_bloated_file()],
            },
        }
        compact_search_files(data)
        f = data["files"]["matches"][0]
        assert "thumb_64" not in f
        assert "id" in f

    def test_passthrough_on_not_ok(self):
        from slack_mcp.compact import compact_search_files
        data = {"ok": False, "error": "invalid_auth"}
        original = copy.deepcopy(data)
        compact_search_files(data)
        assert data == original

    def test_non_dict_matches_do_not_crash(self):
        from slack_mcp.compact import compact_search_files
        data = {
            "ok": True,
            "files": {"matches": ["not_a_dict", None]},
        }
        compact_search_files(data)


# -- compact_search_all --

class TestCompactSearchAll:
    def test_strips_both_messages_and_files(self):
        from slack_mcp.compact import compact_search_all
        msg = _bloated_message()
        msg["channel"] = _bloated_channel_ref()
        data = {
            "ok": True,
            "messages": {
                "total": 1,
                "matches": [msg],
            },
            "files": {
                "total": 1,
                "matches": [_bloated_file()],
            },
        }
        compact_search_all(data)
        assert "blocks" not in data["messages"]["matches"][0]
        assert "thumb_64" not in data["files"]["matches"][0]

    def test_passthrough_on_not_ok(self):
        from slack_mcp.compact import compact_search_all
        data = {"ok": False, "error": "invalid_auth"}
        original = copy.deepcopy(data)
        compact_search_all(data)
        assert data == original


# -- compact_channel_list --

class TestCompactChannelList:
    def test_strips_channels(self):
        from slack_mcp.compact import compact_channel_list
        data = {
            "ok": True,
            "channels": [_bloated_channel()],
        }
        compact_channel_list(data)
        ch = data["channels"][0]
        assert "name_normalized" not in ch
        assert "id" in ch

    def test_passthrough_on_not_ok(self):
        from slack_mcp.compact import compact_channel_list
        data = {"ok": False, "error": "invalid_auth"}
        original = copy.deepcopy(data)
        compact_channel_list(data)
        assert data == original

    def test_missing_channels_key(self):
        from slack_mcp.compact import compact_channel_list
        data = {"ok": True}
        compact_channel_list(data)  # should not raise

    def test_non_dict_channels_do_not_crash(self):
        from slack_mcp.compact import compact_channel_list
        data = {"ok": True, "channels": ["not_a_dict", None]}
        compact_channel_list(data)

    def test_channels_not_a_list(self):
        from slack_mcp.compact import compact_channel_list
        data = {"ok": True, "channels": "not_a_list"}
        compact_channel_list(data)


# -- compact_file_list --

class TestCompactFileList:
    def test_strips_files_list(self):
        from slack_mcp.compact import compact_file_list
        data = {
            "ok": True,
            "files": [_bloated_file(), _bloated_file()],
        }
        compact_file_list(data)
        for f in data["files"]:
            assert "thumb_64" not in f
            assert "id" in f

    def test_strips_single_file(self):
        from slack_mcp.compact import compact_file_list
        data = {
            "ok": True,
            "file": _bloated_file(),
        }
        compact_file_list(data)
        assert "thumb_64" not in data["file"]
        assert "id" in data["file"]

    def test_passthrough_on_not_ok(self):
        from slack_mcp.compact import compact_file_list
        data = {"ok": False, "error": "file_not_found"}
        original = copy.deepcopy(data)
        compact_file_list(data)
        assert data == original

    def test_files_none_does_not_crash(self):
        from slack_mcp.compact import compact_file_list
        data = {"ok": True, "files": None}
        compact_file_list(data)

    def test_files_not_a_list(self):
        from slack_mcp.compact import compact_file_list
        data = {"ok": True, "files": "not_a_list"}
        compact_file_list(data)


# -- compact_items --

class TestCompactItems:
    def test_strips_message_items(self):
        from slack_mcp.compact import compact_items
        data = {
            "ok": True,
            "items": [
                {"type": "message", "message": _bloated_message(), "channel": "C123"},
            ],
        }
        compact_items(data)
        msg = data["items"][0]["message"]
        assert "blocks" not in msg
        assert "ts" in msg

    def test_strips_file_items(self):
        from slack_mcp.compact import compact_items
        data = {
            "ok": True,
            "items": [
                {"type": "file", "file": _bloated_file()},
            ],
        }
        compact_items(data)
        f = data["items"][0]["file"]
        assert "thumb_64" not in f
        assert "id" in f

    def test_passthrough_on_not_ok(self):
        from slack_mcp.compact import compact_items
        data = {"ok": False, "error": "invalid_auth"}
        original = copy.deepcopy(data)
        compact_items(data)
        assert data == original

    def test_missing_items_key(self):
        from slack_mcp.compact import compact_items
        data = {"ok": True}
        compact_items(data)  # should not raise

    def test_non_dict_items_do_not_crash(self):
        from slack_mcp.compact import compact_items
        data = {"ok": True, "items": ["string", None, 42]}
        compact_items(data)  # should not raise

    def test_items_not_a_list(self):
        from slack_mcp.compact import compact_items
        data = {"ok": True, "items": "not_a_list"}
        compact_items(data)  # should not raise

    def test_saved_list_shape(self):
        """saved.list uses top-level 'items' key with nested message/file."""
        from slack_mcp.compact import compact_items
        data = {
            "ok": True,
            "items": [
                {
                    "type": "message",
                    "message": _bloated_message(),
                    "channel": "C123",
                    "date_saved": 1700000000,
                },
            ],
        }
        compact_items(data)
        assert "blocks" not in data["items"][0]["message"]


# -- compact_single_item --

class TestCompactSingleItem:
    def test_strips_top_level_message(self):
        from slack_mcp.compact import compact_single_item
        data = {
            "ok": True,
            "type": "message",
            "channel": "C123",
            "message": _bloated_message(),
        }
        compact_single_item(data)
        msg = data["message"]
        assert "blocks" not in msg
        assert "ts" in msg
        assert "text" in msg

    def test_strips_nested_files_in_message(self):
        from slack_mcp.compact import compact_single_item
        data = {
            "ok": True,
            "type": "message",
            "message": _bloated_message(),
        }
        compact_single_item(data)
        f = data["message"]["files"][0]
        assert "thumb_64" not in f
        assert "id" in f

    def test_passthrough_on_not_ok(self):
        from slack_mcp.compact import compact_single_item
        data = {"ok": False, "error": "channel_not_found"}
        original = copy.deepcopy(data)
        compact_single_item(data)
        assert data == original

    def test_missing_message_key(self):
        from slack_mcp.compact import compact_single_item
        data = {"ok": True, "type": "file", "file": {"id": "F1"}}
        compact_single_item(data)  # should not raise

    def test_strips_file_item(self):
        from slack_mcp.compact import compact_single_item
        data = {
            "ok": True,
            "type": "file",
            "file": _bloated_file(),
        }
        compact_single_item(data)
        assert "thumb_64" not in data["file"]
        assert "id" in data["file"]


# -- decorator registration --

class TestCompactableDecorator:
    def test_registers_compactor(self):
        from slack_mcp.compact import _COMPACTORS, compactable, get_compactor

        def my_compactor(data):
            pass

        @compactable(my_compactor)
        def my_tool():
            pass

        try:
            assert get_compactor("my_tool") is my_compactor
        finally:
            _COMPACTORS.pop("my_tool", None)

    def test_unknown_tool_returns_none(self):
        from slack_mcp.compact import get_compactor
        assert get_compactor("nonexistent_tool_xyz") is None
