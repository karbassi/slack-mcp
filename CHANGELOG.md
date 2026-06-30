# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Six new tools for the personal "what's happening to me" views that the official Slack API doesn't expose — built on the same undocumented session endpoints Slack's own client uses (require `xoxc`+`xoxd` session tokens):
  - `subscriptions_thread_get_view` — your thread inbox with per-thread unread reply counts ("catch me up on my threads").
  - `activity_feed` — your activity inbox: mentions, reactions, replies, reminders, and invites ("what needs my attention").
  - `ai_summarize_unreads_snapshot` — Slack's AI summary of your unread messages ("summarize what I missed").
  - `client_dms` — your open direct messages and group DMs.
  - `slack_lists_get_my_items` — the Slack List tasks and approvals assigned to you.
  - `saved_get` — fetch specific saved-for-later items by id (complements `saved_list`).

### Fixed

- `subscriptions_thread_mark` now form-encodes its request and exposes the required `ts` parameter. Previously it posted a JSON body that Slack ignored, so the call always failed with `invalid_arguments` (issue #56).

## [3.0.0] - 2026-06-29

### Added

- New tools: `blocks_validate`, `assistant_search_context`, `assistant_search_info`, `apps_activities_list`, `oauth_v2_user_access`, and `messages_list` (batch fetch of full message objects by channel and timestamp).
- Per-parameter descriptions for every remaining tool family, extracted from each function's docstring into the MCP tool schema. Building on 2.2.0 (which covered `conversations`, `chat`, and `search`), all tools now expose per-argument guidance to clients.
- Exposed previously-missing optional parameters: PKCE `code_verifier` on `oauth_v2_access` and `openid_connect_token`; `additional_channels`/`enable_section` on `usergroups_create`/`usergroups_update` and `additional_channels`/`is_shared` on `usergroups_users_update`; `archived`/`include_is_subscribed`/`include_archived` on the `slackLists` item and download tools; and `sort_dir` on `assistant_search_context`.

### Fixed

- `tooling_tokens_rotate` now sends only `refresh_token` (was also sending `client_id`/`client_secret`/`grant_type`, which the method does not accept). **Breaking:** the `client_id`/`client_secret`/`grant_type` parameters were removed.
- `entity_present_details` now sends `trigger_id` plus optional `metadata`/`user_auth_required`/`user_auth_url`/`error`. **Breaking:** the previous `app_id`/`entity_id`/`entity_type` parameters (none accepted by the API) were replaced.
- `files_upload_v2` now runs Slack's real upload flow via the slack_sdk helper (`files.upload.v2` is not an HTTP method, so the call always failed). **Breaking:** `content` is now required, `channel_id` became `channel`, and the unused `filetype`/`length` parameters were removed.
- `workflows_featured_add`, `workflows_featured_remove`, and `workflows_featured_set` now send the `channel_id` and `trigger_ids` the Slack Web API actually requires, instead of a bare `workflow_ids` list that would fail.
- Tools forwarding a `dict` or `list` parameter (`blocks`, `attachments`, `view`, `recurrence`, `trigger_ids`, `emails`, …) now send a JSON request body. Form-encoding mangled nested values (a dict collapsed to its first key, a list of dicts to a Python `repr`), so those calls silently sent malformed data.
- Corrected the `chat` streaming tools: `chat_append_stream` and `chat_stop_stream` now use `ts`/`markdown_text` (was `thread_ts`/`text`), `chat_start_stream` exposes the `recipient_user_id`/`recipient_team_id` required for channel streams, and the non-existent `chat_stream` (`chat.stream` is not a Web API method) was removed.
- Corrected `slackLists` tool parameters to match the Slack API: `slack_lists_create` uses `schema`/`description_blocks` (was `columns`/`description`), `slack_lists_items_create` uses `initial_fields` (was `column_values`), `slack_lists_items_update` uses `cells` (was `item_id`/`column_values`), and `slack_lists_update` uses `description_blocks`. Previously the field data was silently dropped.
- Corrected `conversations` shared-invite tools: `conversations_request_shared_invite_approve` drops the unsupported `is_approved` and adds `is_external_limited`; `conversations_external_invite_permissions_set` adds the required `target_team`; and `conversations_request_shared_invite_deny`'s `message` is now a string (the API rejects an object there).
- `users_get_presence`'s `user` argument is now optional (defaults to the authenticated user, matching the API). `functions_complete_success` now requires `outputs` (the API requires it). **Breaking:** `users_set_photo` now takes `image_base64` (base64-encoded image bytes, uploaded via multipart) instead of `image` — the old form-string path could never upload a real image.
- `drafts_delete` no longer raises `KeyError` on a malformed `drafts.list` entry while auto-fetching the latest timestamp.

### Internal

- Added the `ty` type checker (`mise run typecheck`, included in `mise run check`) and pre-commit hooks.

## [2.2.0] - 2026-06-15

### Added

- Per-parameter descriptions for the `conversations`, `chat`, and `search` tool families, extracted from each function's docstring into the MCP tool schema (FastMCP 3.x docstring parsing) so clients get per-argument guidance.
- 30-second timeout on the slow paginated read tools (`search_all`, `search_files`, `search_messages`, `conversations_history`, `conversations_replies`) so a hung Slack call can't hang the client.

### Changed

- Slack `ok:false` responses are now surfaced as MCP tool errors via `ToolResult.is_error` (an outermost middleware) instead of being reported as successful calls — primarily affects the undocumented/session endpoints (official methods already raised).
- Widened nested-object tool parameter types from `dict[str, str]` to `dict[str, Any]` (`views.view`, workflow `inputs`/`outputs`/`error`, and canvas `changes`/`criteria`/`document_content`) so real Slack payloads are no longer rejected at the MCP schema boundary.
- Require `fastmcp>=3.4.2`, which pulls the `starlette>=1.0.1` floor (CVE-2026-48710).

### Internal

- Tool tests now drive the assembled server through an in-memory FastMCP `Client`, exercising schema validation, the middleware stack, and serialization (the change that surfaced the nested-type widening above).

## [2.1.0] - 2026-06-04

### Added

- User-object compaction for `users_info`, `users_list`, `users_lookup_by_email`, and `users_profile_get` — strips avatar-size variants, normalized name duplicates, status display info, timezone offsets, and other profile bloat (keeps one canonical avatar). Set `detailed=True` for the full response.
- Reaction and channel topic/purpose compaction — reaction `users` ID arrays are trimmed to `{name, count}`, and channel `topic`/`purpose` to just their `.value`.

### Changed

- Cross-cutting tool behavior is now declared at each tool instead of in remote lists: cache TTL via `meta={"cache_ttl": ...}` and name-resolution opt-out via a `"skip-resolution"` tag, read by middleware at call time. No API changes.
- Internal refactors with no API changes: `SlackClient` omits `None` keyword arguments so tools forward parameters unconditionally; Slack error-string classification centralized in `slack_mcp.errors`; draft-body composition deduplicated behind `_draft_body`.

### Fixed

- Close the httpx session client on server shutdown via the FastMCP lifespan, so session connections are no longer leaked on exit.

## [2.0.0] - 2026-04-03

### Added

- Compact response middleware — automatically strips bloat from Slack API responses (blocks, attachments, thumbnails, metadata) using allowlist-based field stripping
- `@compactable` decorator for registering tools with response compactors
- `detailed` parameter on 15 tools — set `detailed=True` to bypass compaction and get the full Slack API response
- Compactable tools: `search_messages`, `search_all`, `search_files`, `conversations_history`, `conversations_replies`, `conversations_list`, `files_list`, `files_info`, `pins_list`, `reactions_list`, `reactions_get`, `stars_list`, `search_modules_messages`, `conversations_view`, `saved_list`

### Changed

- `search_messages` `compact` parameter replaced by `detailed` (inverted semantics: compaction is now the default, opt out with `detailed=True`)
- Middleware ordering optimized — compaction runs before name resolution so fewer IDs need resolving
- Thread cache keys treat `detailed=False` the same as omitting `detailed`, while `detailed=True` produces a separate cache entry to avoid mixing compacted and full responses

## [1.3.1] - 2026-03-24

### Fixed

- Name resolution middleware now works with Claude Code and other MCP clients that read `structuredContent` instead of `content[0].text`
- Cache is now namespaced by token hash so multiple workspace instances don't share cached responses

### Changed

- Full type annotations on all tool parameters (`list` → `list[str]`, `dict` → `dict[str, str]`, etc.)
- Fixed all ruff E501 line-length warnings

### Removed

- Stale "Known Issues" note about FastMCP middleware bug — resolved by using `structured_content` per FastMCP docs

## [1.3.0] - 2026-03-22

### Added

- 22 new undocumented session endpoint tools:
  - **Drafts**: `drafts.create`, `drafts.update`, `drafts.delete` — full draft lifecycle; `drafts.list` now supports `is_active` and `limit` params
  - **Saved items**: `saved.add`, `saved.delete` — manage "Save for later" items
  - **Emoji**: `emoji.add`, `emoji.remove`, `emoji.adminList` — workspace-level emoji management
  - **Granular search**: `search.modules.messages`, `search.modules.files`, `search.modules.channels`, `search.modules.people`, `search.modules.dms`
  - **Conversations**: `conversations.view`, `conversations.listPrefs` — read state and notification preferences
  - **Users**: `users.channelSections.list`, `users.priority.list` — sidebar organization and contact ranking
  - **Threads**: `subscriptions.thread.mark` — mark threads as read/unread
  - **Workspace**: `experiments.getByUser`, `api.features`, `aiApps.list`
- `session_call_multipart` client method for multipart form uploads
- Generic ID resolution for all tool responses — user, channel, DM, and bot IDs are auto-resolved to display names via `resolved_names` (not just message tools)
- Disk-cached resolver lookups — users/bots cached 1hr, channels 5min, same DiskStore as response cache
- Platform-native cache directory via `platformdirs` (`~/Library/Caches` on macOS, `~/.cache` on Linux), with `XDG_CACHE_HOME` override
- `CLAUDE.md` with project instructions
- Integration tests for all 220 tools (342 pass, ~68 skipped with documented reasons)
- Test fixture PNG for emoji upload tests

### Fixed

- `session_call_form` now sets `charset=utf-8` in Content-Type to avoid `missing_charset` warnings
- Draft `client_last_updated_ts` padded to 7 decimal places to prevent `draft_has_conflict` errors
- ID resolver regex updated to match documented Slack ID formats (D/Z prefixes, 8+ char minimum)

## [1.1.0] - 2026-03-22

### Added

- `resolve_names` tool — bulk-resolve user and channel IDs to display names in a single call with concurrent lookups, bounded concurrency, and input deduplication
- `NameResolutionMiddleware` — automatically resolves user, channel, and bot IDs to display names in responses from `conversations_history`, `conversations_replies`, `search_messages`, and `search_all`

## [1.0.0] - 2026-02-24

### Added

- Response caching middleware — stable identity data (users, teams, bots, emoji) cached for 1 hour, dynamic data (channel lists, members, bookmarks) cached for 5 minutes
- `ThreadCachingMiddleware` — automatically caches `conversations_replies` for threads older than 1 hour and `conversations_history` for bounded historical ranges
- `cache_clear` tool — clears the entire MCP cache on demand so subsequent calls fetch fresh data
- `py-key-value-aio[disk]` dependency for disk-backed caching
- Ruff linter/formatter configuration
- CHANGELOG and CONTRIBUTING guide
- Security policy

### Fixed

- Session token fallback for `conversations.mark`
- `SlackApiError` handling for session token fallback

## [0.1.0] - 2026-02-07

Initial release.

### Added

- 193 tools across 35 Slack API families
- Full Slack Web API coverage: messages, channels, files, search, reactions, pins, stars, reminders, DND, calls, canvases, lists, workflows, user groups, and more
- 4 undocumented session endpoints (`client.boot`, `client.counts`, `client.userBoot`, `threads.getView`)
- 11 legacy undocumented endpoints (`chat.command`, `files.edit`, `bots.list`, etc.)
- SlackClient with 4 transport methods (form/JSON x official/session)
- FastMCP 3.0 integration with dependency injection
- Slack app manifest with all required OAuth scopes
- Unit tests with mocked client for all tool families
- Integration tests against live Slack API
- `uvx` support for zero-install usage
- README with quickstart, setup, and architecture documentation
- MIT license
