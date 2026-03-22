# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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

### Known Issues

- `resolved_names` middleware injection is silently discarded by FastMCP ([prefecthq/fastmcp#3590](https://github.com/prefecthq/fastmcp/issues/3590)). Resolver logic and caching work correctly; names will appear in responses once upstream is fixed.

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
