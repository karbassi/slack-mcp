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
        "reactions": [
            {"name": "thumbsup", "count": 2, "users": ["U1", "U2"]},
        ],
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
        # shared-message unfurl: content lives here, bloat surrounds it
        "attachments": [
            {
                "author_subname": "Bob",
                "text": "the shared message body",
                "from_url": "https://slack.com/archives/C1/p1",
                "ts": "1234560000.000000",
                # bloat:
                "fallback": "the shared message body",
                "blocks": [{"type": "rich_text"}],
                "color": "D0D0D0",
                "footer": "Slack Conversation",
                "work_object_entity": {"layouts": {"expanded": {}}},
                "files": [
                    {"id": "F9", "name": "shared.pdf", "thumb_64": "https://t64"}
                ],
            }
        ],
        # bloat fields:
        "blocks": [{"type": "rich_text"}],
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
        "topic": {
            "value": "General chat",
            "creator": "U001",
            "last_set": 1700000000,
        },
        "purpose": {
            "value": "A place for everything",
            "creator": "U001",
            "last_set": 1700000000,
        },
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


def _bloated_user():
    return {
        "id": "U002",
        "name": "jane.doe",
        "real_name": "Jane Doe",
        "team_id": "T002",
        "deleted": False,
        "is_bot": False,
        "is_app_user": False,
        "is_admin": False,
        "is_owner": False,
        "is_primary_owner": False,
        "is_restricted": False,
        "is_ultra_restricted": False,
        "is_email_confirmed": True,
        "tz": "America/Chicago",
        "tz_label": "Central Daylight Time",
        "profile": {
            "real_name": "Jane Doe",
            "display_name": "Jane Doe",
            "email": "jane.doe@example.com",
            "title": "Associate Dir, Systems Ops",
            "phone": "",
            "pronouns": "she/they",
            "first_name": "Jane",
            "last_name": "Doe",
            "status_text": "",
            "status_emoji": "",
            "status_expiration": 0,
            "image_512": "https://avatars.slack-edge.com/x_512.jpg",
            # bloat:
            "avatar_hash": "00000000aaaa",
            "real_name_normalized": "Jane Doe",
            "display_name_normalized": "Jane Doe",
            "image_24": "https://avatars.slack-edge.com/x_24.jpg",
            "image_32": "https://avatars.slack-edge.com/x_32.jpg",
            "image_48": "https://avatars.slack-edge.com/x_48.jpg",
            "image_72": "https://avatars.slack-edge.com/x_72.jpg",
            "image_192": "https://avatars.slack-edge.com/x_192.jpg",
            "image_1024": "https://avatars.slack-edge.com/x_1024.jpg",
            "image_original": "https://avatars.slack-edge.com/x_original.jpg",
            "is_custom_image": True,
            "status_emoji_display_info": [],
            "status_text_canonical": "",
            "huddle_state": "default_unset",
            "team": "T002",
            "start_date": "2026-04-28",
        },
        # bloat:
        "color": "7d414c",
        "updated": 1780409890,
        "tz_offset": -18000,
        "who_can_share_contact_card": "EVERYONE",
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
        assert "client_msg_id" not in msg
        assert "team" not in msg

    def test_keeps_lean_attachment_content(self):
        from slack_mcp.compact import strip_message
        msg = _bloated_message()
        strip_message(msg)
        att = msg["attachments"][0]
        # content survives so models don't escalate to detailed=True
        assert att["author_subname"] == "Bob"
        assert att["text"] == "the shared message body"
        assert att["from_url"] == "https://slack.com/archives/C1/p1"
        # bloat is gone
        assert "fallback" not in att
        assert "blocks" not in att
        assert "color" not in att
        assert "footer" not in att
        assert "work_object_entity" not in att
        # nested files are stripped, not dropped
        f = att["files"][0]
        assert f["id"] == "F9"
        assert "thumb_64" not in f

    def test_strips_nested_files(self):
        from slack_mcp.compact import strip_message
        msg = _bloated_message()
        strip_message(msg)
        f = msg["files"][0]
        assert "id" in f
        assert "name" in f
        assert "thumb_64" not in f
        assert "thumb_80" not in f

    def test_strips_reaction_user_arrays(self):
        from slack_mcp.compact import strip_message
        msg = _bloated_message()
        strip_message(msg)
        reaction = msg["reactions"][0]
        assert reaction == {"name": "thumbsup", "count": 2}
        assert "users" not in reaction

    def test_reactions_non_list_does_not_crash(self):
        from slack_mcp.compact import strip_message
        msg = {"ts": "1", "text": "hi", "reactions": "nope"}
        strip_message(msg)
        assert "ts" in msg

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

    def test_attachments_non_list_is_dropped(self):
        from slack_mcp.compact import strip_message
        msg = {"ts": "1", "text": "hi", "attachments": None}
        strip_message(msg)
        assert "ts" in msg
        # present-but-not-a-list is dropped, not emitted as attachments: None
        assert "attachments" not in msg

    def test_attachments_with_non_dict_elements(self):
        from slack_mcp.compact import strip_message
        msg = {"ts": "1", "text": "hi", "attachments": ["nope", None, 7]}
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


# -- strip_attachment --

class TestStripAttachment:
    def test_keeps_content_strips_bloat(self):
        from slack_mcp.compact import strip_attachment
        a = {
            "author_subname": "Bob",
            "text": "shared body",
            "from_url": "https://x/1",
            "color": "D0D0D0",
            "blocks": [{"type": "rich_text"}],
        }
        strip_attachment(a)
        assert a["author_subname"] == "Bob"
        assert a["text"] == "shared body"
        assert "color" not in a
        assert "blocks" not in a

    def test_strips_nested_files(self):
        from slack_mcp.compact import strip_attachment
        a = {"text": "x", "files": [{"id": "F1", "name": "d.pdf", "thumb_64": "t"}]}
        strip_attachment(a)
        assert a["files"][0]["id"] == "F1"
        assert "thumb_64" not in a["files"][0]

    def test_files_non_list_is_dropped(self):
        from slack_mcp.compact import strip_attachment
        a = {"text": "x", "files": None}
        strip_attachment(a)
        assert a["text"] == "x"
        assert "files" not in a


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

    def test_trims_topic_and_purpose_to_value(self):
        from slack_mcp.compact import strip_channel
        ch = _bloated_channel()
        strip_channel(ch)
        assert ch["topic"] == {"value": "General chat"}
        assert ch["purpose"] == {"value": "A place for everything"}

    def test_non_dict_topic_does_not_crash(self):
        from slack_mcp.compact import strip_channel
        ch = {"id": "C1", "name": "x", "topic": None, "purpose": "str"}
        strip_channel(ch)
        assert ch["id"] == "C1"


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


# -- strip_user --

class TestStripUser:
    def test_keeps_allowed_fields(self):
        from slack_mcp.compact import strip_user
        u = _bloated_user()
        strip_user(u)
        assert "id" in u
        assert "name" in u
        assert "real_name" in u
        assert "tz" in u
        assert "profile" in u

    def test_removes_bloat(self):
        from slack_mcp.compact import strip_user
        u = _bloated_user()
        strip_user(u)
        assert "color" not in u
        assert "updated" not in u
        assert "tz_offset" not in u
        assert "who_can_share_contact_card" not in u

    def test_strips_nested_profile(self):
        from slack_mcp.compact import strip_user
        u = _bloated_user()
        strip_user(u)
        p = u["profile"]
        assert "email" in p
        assert "title" in p
        assert "image_512" in p
        assert "image_24" not in p
        assert "image_1024" not in p
        assert "avatar_hash" not in p
        assert "real_name_normalized" not in p
        assert "status_emoji_display_info" not in p

    def test_profile_none_does_not_crash(self):
        from slack_mcp.compact import strip_user
        u = {"id": "U1", "profile": None, "color": "abc"}
        strip_user(u)
        assert "id" in u
        assert "color" not in u


# -- compact_users --

class TestCompactUsers:
    def test_strips_single_user(self):
        from slack_mcp.compact import compact_users
        data = {"ok": True, "user": _bloated_user()}
        compact_users(data)
        u = data["user"]
        assert "color" not in u
        assert "image_24" not in u["profile"]
        assert "email" in u["profile"]

    def test_strips_members_list(self):
        from slack_mcp.compact import compact_users
        data = {"ok": True, "members": [_bloated_user(), _bloated_user()]}
        compact_users(data)
        for m in data["members"]:
            assert "tz_offset" not in m
            assert "image_1024" not in m["profile"]

    def test_strips_bare_profile(self):
        from slack_mcp.compact import compact_users
        data = {"ok": True, "profile": _bloated_user()["profile"]}
        compact_users(data)
        assert "avatar_hash" not in data["profile"]
        assert "email" in data["profile"]

    def test_passthrough_on_not_ok(self):
        from slack_mcp.compact import compact_users
        data = {"ok": False, "error": "users_not_found"}
        original = copy.deepcopy(data)
        compact_users(data)
        assert data == original

    def test_missing_keys_do_not_crash(self):
        from slack_mcp.compact import compact_users
        compact_users({"ok": True})

    def test_members_not_a_list(self):
        from slack_mcp.compact import compact_users
        compact_users({"ok": True, "members": "not_a_list"})

    def test_non_dict_members_do_not_crash(self):
        from slack_mcp.compact import compact_users
        compact_users({"ok": True, "members": ["str", None, 42]})


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


# -- compact_messages_by_channel --

class TestCompactMessagesByChannel:
    def test_strips_messages_keyed_by_channel(self):
        from slack_mcp.compact import compact_messages_by_channel
        data = {
            "ok": True,
            "messages": {"C123": [_bloated_message(), _bloated_message()]},
        }
        compact_messages_by_channel(data)
        for msg in data["messages"]["C123"]:
            assert "blocks" not in msg
            assert "ts" in msg

    def test_passthrough_on_not_ok(self):
        from slack_mcp.compact import compact_messages_by_channel
        data = {"ok": False, "error": "channel_not_found"}
        original = copy.deepcopy(data)
        compact_messages_by_channel(data)
        assert data == original

    def test_missing_messages_key(self):
        from slack_mcp.compact import compact_messages_by_channel
        data = {"ok": True}
        compact_messages_by_channel(data)  # should not raise


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
