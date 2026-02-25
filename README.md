<div align="center">

# Slack MCP

**Your entire Slack workspace — available to any AI.**

[![Python](https://img.shields.io/pypi/pyversions/slack-mcp?style=flat-square)](https://pypi.org/project/slack-mcp/)
[![License](https://img.shields.io/github/license/karbassi/slack-mcp?style=flat-square)](LICENSE)

A [Model Context Protocol](https://modelcontextprotocol.io/) server that gives LLMs full access to [Slack](https://slack.com).<br>
Messages, channels, files, canvases, lists, search, reactions — all of it.

**193 tools** · **35 API families** · **Every Slack feature**

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
| **Conversations** | 28 | History, threads, replies, create, archive, invite, mark read |
| **Files** | 16 | Upload, share, edit, list, remote files |
| **Chat** | 14 | Send, reply, schedule, update, delete, ephemeral |
| **Users** | 12 | Profile, presence, lookup, list |
| **Lists** | 12 | Create, edit items, manage access |
| **Legacy** | 11 | Slash commands, file editing, bot listing |
| **Team** | 9 | Info, preferences, access logs, billing |
| **Apps** | 8 | Manifests, connections, authorizations |
| **Usergroups** | 7 | Create, update, manage members |
| **Workflows** | 7 | Featured workflows, step completion |
| **Canvases** | 6 | Create, edit, sections, access control |
| **Calls** | 6 | Start, end, manage participants |
| **+ 23 more** | | DND, reminders, bookmarks, reactions, pins, stars, views, search, auth, bots, emoji, ... |

Plus a `cache_clear` utility tool to bust the response cache on demand.

### Beyond the Official API

15 undocumented and legacy endpoints — the same internal APIs that Slack's own apps use. Requires session tokens (`xoxc`+`xoxd`).

<details>
<summary><strong>Session endpoints</strong> — workspace state the official API doesn't expose</summary>

| Endpoint | What it provides |
|---|---|
| `client.boot` | Full workspace bootstrap — channels, users, prefs, feature flags |
| `client.counts` | Unread counts per channel/DM/thread plus mention counts |
| `client.userBoot` | User-specific bootstrap data scoped to the authenticated user |
| `threads.getView` | Thread inbox — the list of threads with read/unread state |

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

</details>

## Authentication

| Variable | Required | Description |
|---|---|---|
| `SLACK_XOXP_TOKEN` | **Yes** | User OAuth token from your Slack app |
| `SLACK_XOXC_TOKEN` | No | Browser session token for undocumented endpoints |
| `SLACK_XOXD_TOKEN` | No | Browser session cookie (paired with `xoxc`) |

> **Official vs session:** The `xoxp` token covers all 193 official API tools. For undocumented endpoints (unread counts, workspace boot, file editing), you also need `xoxc`+`xoxd` — grab them from your browser cookies while logged into slack.com.

## Caching

Responses are cached automatically to reduce API calls:

- **Stable data** (users, teams, bots, emoji) — 1 hour TTL
- **Dynamic data** (channel lists, members, bookmarks) — 5 minute TTL
- **Old threads** (`conversations_replies` with ts > 1 hour old) — 1 hour TTL
- **Bounded history** (`conversations_history` with old date range) — 1 hour TTL

Use the `cache_clear` tool to bust the cache when you need fresh data.

## Development

```bash
git clone https://github.com/karbassi/slack-mcp.git
cd slack-mcp
uv sync
uv run ruff check .
uv run pytest tests/
uv run pytest tests/ -m integration  # requires tokens in .env
```

## License

[MIT](LICENSE)
