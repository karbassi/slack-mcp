<div align="center">

# Slack MCP

**Your entire Slack workspace — available to any AI.**

[![Python](https://img.shields.io/pypi/pyversions/slack-mcp?style=flat-square)](https://pypi.org/project/slack-mcp/)
[![License](https://img.shields.io/github/license/karbassi/slack-mcp?style=flat-square)](LICENSE)

A [Model Context Protocol](https://modelcontextprotocol.io/) server that gives LLMs full access to [Slack](https://slack.com).<br>
Messages, channels, files, canvases, lists, search, reactions — all of it.

**253 tools** · **37 API families** · **Every Slack feature**

</div>

---

## Quick Start

### 1. Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps) > **Create New App** > **From a manifest**
2. Paste the contents of [`manifest.json`](manifest.json)
3. Install to your workspace
4. Copy the **User OAuth Token** (`xoxp-...`) from **OAuth & Permissions**

### 2. Add to your AI client

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude mcp add slack -- uvx --from git+https://github.com/karbassi/slack-mcp.git slack-mcp
```

Then set `SLACK_XOXP_TOKEN` in your shell environment.

</details>

<details>
<summary><strong>Claude Desktop</strong></summary>

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/karbassi/slack-mcp.git", "slack-mcp"],
      "env": {
        "SLACK_XOXP_TOKEN": "xoxp-..."
      }
    }
  }
}
```

</details>

<details>
<summary><strong>Cursor</strong></summary>

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/karbassi/slack-mcp.git", "slack-mcp"],
      "env": {
        "SLACK_XOXP_TOKEN": "xoxp-..."
      }
    }
  }
}
```

</details>

<details>
<summary><strong>Windsurf</strong></summary>

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/karbassi/slack-mcp.git", "slack-mcp"],
      "env": {
        "SLACK_XOXP_TOKEN": "xoxp-..."
      }
    }
  }
}
```

</details>

<details>
<summary><strong>VS Code / GitHub Copilot</strong></summary>

Add to your VS Code `settings.json`:

```json
{
  "mcp": {
    "servers": {
      "slack": {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/karbassi/slack-mcp.git", "slack-mcp"],
        "env": {
          "SLACK_XOXP_TOKEN": "xoxp-..."
        }
      }
    }
  }
}
```

</details>

<details>
<summary><strong>Local clone</strong></summary>

```json
{
  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--directory", "/path/to/slack-mcp", "slack-mcp"]
    }
  }
}
```

</details>

## What Can It Do?

> *"Catch me up on #engineering from today"*
> *"Reply to Sarah's thread saying we'll ship it Monday"*
> *"Search for anything about the Q3 roadmap"*
> *"Create a channel called #project-atlas and invite the design team"*

| Domain | Tools | Highlights |
|---|---|---|
| **Conversations** | 31 | History, threads, replies, create, archive, invite, mark read, team connections, suggestions |
| **Undocumented** | 38 | Drafts, saved items, emoji management, granular search, sidebar, threads, activity inbox, DMs, AI unread summary + digests, Today view, Connect invites |
| **Files** | 19 | Upload, share, edit, list, remote files, shares, recently deleted, favorites |
| **Chat** | 13 | Send, reply, schedule, update, delete, ephemeral, stream |
| **Users** | 15 | Profile, presence, lookup, list, profile extras/sections, custom statuses |
| **Lists** | 15 | Create, edit items, manage access, my assigned items, templates, records |
| **Legacy** | 11 | Slash commands, file editing, bot listing |
| **Team** | 9 | Info, preferences, access logs, billing |
| **Apps** | 9 | Manifests, connections, authorizations, activities |
| **Workflows** | 8 | Featured workflows, step completion, workflow/trigger listing |
| **Usergroups** | 7 | Create, update, manage members |
| **Canvases** | 7 | Create, edit, sections, access control, templates |
| **Calls** | 6 | Start, end, manage participants |
| **+ 24 more** | | Calendar, DND, reminders, bookmarks, reactions, pins, stars, views, search, auth, bots, emoji, ... |

Plus `resolve_names` (bulk ID→name resolution) and `cache_clear` (bust the response cache on demand) utility tools.

### Beyond the Official API

68 undocumented and legacy endpoints — the same internal APIs that Slack's own apps use. Requires session tokens (`xoxc`+`xoxd`).

<details>
<summary><strong>Session endpoints</strong> — workspace state the official API doesn't expose</summary>

| Endpoint | What it provides |
|---|---|
| `client.boot` | Full workspace bootstrap — channels, users, prefs, feature flags |
| `client.counts` | Unread counts per channel/DM/thread plus mention counts |
| `client.userBoot` | User-specific bootstrap data scoped to the authenticated user |
| `threads.getView` | Thread inbox — the list of threads with read/unread state |
| `subscriptions.thread.getView` | My threads with unread reply counts — "catch me up on my threads" |
| `subscriptions.thread.mark` | Mark individual threads as read or unread |
| `client.dms` | Open DMs and group DMs (`ims` + `mpims`) |
| `activity.feed` | Activity inbox — mentions, reactions, replies, reminders, invites |
| `drafts.list` | List all unsent message drafts |
| `drafts.create` | Create a message draft with Block Kit text |
| `drafts.update` | Edit an existing draft |
| `drafts.delete` | Delete a draft |
| `saved.list` | List saved-for-later items |
| `saved.get` | Fetch specific saved-for-later items by id |
| `saved.add` | Save a message for later with optional due date |
| `saved.delete` | Remove a saved-for-later item |
| `lists.getMyItems` | Slack List tasks and approvals assigned to me |
| `emoji.add` | Add a custom emoji from a URL |
| `emoji.remove` | Remove a custom emoji |
| `emoji.adminList` | Emoji with rich metadata — uploader, date, usage stats |
| `search.modules.messages` | Granular message search |
| `search.modules.files` | File-specific search |
| `search.modules.channels` | Server-side channel search by name or topic |
| `search.modules.people` | Fuzzy people search by name, title, department |
| `search.modules.dms` | Search within DMs only |
| `conversations.view` | Channel view with read state and personal config |
| `conversations.listPrefs` | Per-channel notification and mute preferences |
| `users.channelSections.list` | Sidebar organization — custom sections, favorites |
| `users.priority.list` | Contacts ranked by interaction frequency |
| `experiments.getByUser` | A/B test experiment assignments |
| `api.features` | Workspace feature flags |
| `aiApps.list` | AI applications configured in the workspace |
| `ai.alpha.summarize.unreadsSnapshot` | AI summary of unread messages — "summarize what I missed" |
| `ai.alpha.digest.list` | Slack's AI recaps/digests of activity across channels |
| `subscriptions.thread.get` | Subscription/read state for a single thread |
| `today.items.list` | Today view items (suggested to-dos, highlights) |
| `connectInvites.list` | Pending Slack Connect channel and DM invites |
| `conversations.teamConnections` | Slack Connect connections for a channel |
| `conversations.suggestions` | Suggested channels for the user |
| `conversations.bulkReacjiTriggers` | Per-channel reacji (auto-reaction) triggers |
| `lists.templates` | Available Slack List templates |
| `lists.records.list` | Records/items within a given Slack List |
| `calendar.getInstalledCalendars` | Connected calendars (`gcal`, `ocal`) |
| `calendar.user.status` | The user's current calendar status |
| `canvases.getCannedTemplates` | Available canvas templates |
| `emoji.collections.list` | Installed and available emoji packs |
| `files.getShares` | Where a file is shared (channels, tabs, viewer count) |
| `files.recentlyDeleted` | Recently deleted files |
| `files.favorites.list` | Favorited files |
| `functions.workflows.list` | Workflows and their triggers |
| `workflows.triggers.list` | Triggers, filterable by app |
| `users.profile.getExtras` | Profile extras — shared channels, onboarding state |
| `users.profile.getSections` | Custom profile sections |
| `users.customStatus.list` | Saved and scheduled custom statuses |
| `search.inline` | Inline/quick search scoped to a channel or user |
| `search.save` | Save a search |
| `enterpriseSearch.getConnectors` | Configured enterprise search connectors |

</details>

<details>
<summary><strong>Legacy endpoints</strong> — functionality missing from the official API</summary>

| Endpoint | What it provides |
|---|---|
| `chat.command` | Execute slash commands programmatically |
| `commands.list` | List all slash commands including custom ones |
| `files.edit` | Edit a file's title, content, or filetype in-place |
| `files.share` | Share a file to a channel |
| `bots.list` | List all bot users in the workspace |
| `team.prefs.get` | Team-level preferences — retention, permissions, domains |
| `users.prefs.get` | All user preferences — notifications, sidebar, theme |
| `users.prefs.set` | Set any individual user preference |
| `users.admin.invite` | Invite users by email (Enterprise Grid) |
| `users.admin.setInactive` | Deactivate a user account (Enterprise Grid) |
| `channels.delete` | Dead method — included for completeness |

> [!WARNING]
> Undocumented endpoints can break without notice. They use session tokens (`xoxc`+`xoxd`) which expire and must be re-grabbed from browser cookies.

</details>

## Authentication

| Variable | Required | Description |
|---|---|---|
| `SLACK_XOXP_TOKEN` | **Yes** | User OAuth token from your Slack app |
| `SLACK_XOXC_TOKEN` | No | Browser session token for undocumented endpoints |
| `SLACK_XOXD_TOKEN` | No | Browser session cookie (paired with `xoxc`) |

> [!TIP]
> The `xoxp` token covers all Slack Web API tools. Utility tools like `resolve_names` and `cache_clear` work without additional auth. For undocumented endpoints (unread counts, workspace boot, file editing), you also need `xoxc`+`xoxd` — grab them from your browser cookies while logged into slack.com.

## Caching

Responses are cached automatically to reduce API calls:

- **Stable data** (users, teams, bots, emoji) — 1 hour TTL
- **Dynamic data** (channel lists, members, bookmarks) — 5 minute TTL
- **Old threads** (`conversations_replies` with ts > 1 hour old) — 1 hour TTL
- **Bounded history** (`conversations_history` with old date range) — 1 hour TTL
- **Resolved names** (user/bot → 1 hour, channel → 5 minutes)

Cache is stored at the platform-native location (`~/Library/Caches/slack-mcp` on macOS, `~/.cache/slack-mcp` on Linux). Set `XDG_CACHE_HOME` to override.

Use the `cache_clear` tool to bust the cache when you need fresh data.

### Name Resolution

All tool responses automatically resolve user, channel, DM, and bot IDs to display names via a `resolved_names` field — no extra tool calls needed. Resolved names are disk-cached to avoid redundant API lookups.

### Response Compaction

15 high-volume tools automatically strip bloat from Slack API responses — blocks (duplicates text), attachments (link unfurls), thumbnails (22 per file), and metadata noise. Measured reductions:

| Endpoint | Before | After | Reduction |
|---|---|---|---|
| `conversations.history` | 465 KB | 113 KB | **76%** |
| `files.list` | 127 KB | 26 KB | **80%** |
| `conversations.list` | 59 KB | 17 KB | **71%** |
| `reactions.list` | 353 KB | 167 KB | **53%** |

Compaction is on by default. Pass `detailed=True` to any compactable tool to get the full Slack API response.

## Development

```bash
git clone https://github.com/karbassi/slack-mcp.git
cd slack-mcp
uv sync
uv run pre-commit install            # ruff + ty on every commit
mise run check                       # test + lint + security scan
mise run test:integration            # requires tokens in .env
```

> [!NOTE]
> ~68 integration tests are skipped because they require a bot token (`xoxb`), Slack Connect, interactive triggers (e.g. `views.open`), or would be destructive (e.g. `auth.revoke`). Adding bot token support is a future goal.

## License

[MIT](LICENSE)
