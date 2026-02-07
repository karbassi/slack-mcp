# Slack MCP

The most complete Slack integration for AI agents. **193 tools** covering the entire Slack Web API — messages, channels, files, canvases, lists, search, reactions, and more — all accessible through the [Model Context Protocol](https://modelcontextprotocol.io/).

Give your AI assistant full access to Slack. Read unread messages, draft replies, search across your workspace, manage channels, upload files, set reminders — anything you can do in Slack, your agent can do too.

## Quickstart

One command. No cloning needed.

Add to your MCP client config (`.mcp.json` for Claude Code, `claude_desktop_config.json` for Claude Desktop):

```json
{
  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/karbassi/slack-api.git", "slack-mcp"],
      "env": {
        "SLACK_XOXP_TOKEN": "xoxp-..."
      }
    }
  }
}
```

That's it. Your agent now has Slack.

## What can it do?

**Read** — Unread messages, channel history, threads, search results, file listings

**Write** — Send messages, reply to threads, react, pin, bookmark, schedule messages

**Manage** — Create/archive channels, invite users, set topics, manage user groups

**Files** — Upload, share, edit, organize across channels

**Advanced** — Canvases, Lists, Reminders, Do Not Disturb, Calls, Workflows

Plus undocumented endpoints like `client.counts` for unread badges and `client.boot` for workspace state — things even Slack's own app uses internally.

### 193 tools across 35 API families

| Family | Tools | Family | Tools |
|--------|-------|--------|-------|
| conversations | 28 | files | 16 |
| chat | 14 | users | 12 |
| slack_lists | 12 | legacy | 11 |
| team | 9 | apps | 8 |
| usergroups | 7 | workflows | 7 |
| canvases | 6 | calls | 6 |
| dnd | 5 | reminders | 5 |
| bookmarks | 4 | reactions | 4 |
| views | 4 | undocumented | 4 |
| auth | 3 | assistant | 3 |
| oauth | 3 | pins | 3 |
| search | 3 | stars | 3 |
| bots | 2 | functions | 2 |
| openid | 2 | rtm | 2 |
| api | 1 | dialog | 1 |
| emoji | 1 | entity | 1 |
| migration | 1 | tooling | 1 |

## Setup

### 1. Create a Slack App

Use the included `manifest.json` to create a Slack app with all required scopes pre-configured:

1. Go to [api.slack.com/apps](https://api.slack.com/apps) > **Create New App** > **From a manifest**
2. Paste the contents of `manifest.json`
3. Install to your workspace
4. Copy the **User OAuth Token** (`xoxp-...`) from **OAuth & Permissions**

### 2. Set your token

The only required token is `SLACK_XOXP_TOKEN`. Set it in your MCP config's `env` block (see Quickstart above), or via a `.env` file if running locally.

For access to undocumented endpoints (unread counts, workspace boot, file editing), you'll also need session tokens from your browser:

| Token | Source | Required |
|-------|--------|----------|
| `SLACK_XOXP_TOKEN` | Slack app OAuth | Yes |
| `SLACK_XOXC_TOKEN` | Browser cookies | Optional |
| `SLACK_XOXD_TOKEN` | Browser cookies | Optional |

## Install

### Via uvx (recommended)

No install step — `uvx` handles it. See [Quickstart](#quickstart).

### From git

```sh
uv pip install git+https://github.com/karbassi/slack-api.git
```

### From a local clone

```sh
git clone https://github.com/karbassi/slack-api.git
cd slack-api
uv sync
```

## Usage

### MCP server (uvx)

```json
{
  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/karbassi/slack-api.git", "slack-mcp"],
      "env": {
        "SLACK_XOXP_TOKEN": "xoxp-...",
        "SLACK_XOXC_TOKEN": "xoxc-...",
        "SLACK_XOXD_TOKEN": "xoxd-..."
      }
    }
  }
}
```

### MCP server (local clone)

```json
{
  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--directory", "/path/to/slack-api", "slack-mcp"]
    }
  }
}
```

### Standalone

```sh
slack-mcp
```

## Architecture

Built with [FastMCP 3.0](https://github.com/jlowin/fastmcp) and [slack-sdk](https://github.com/slackapi/python-slack-sdk).

```
src/slack_mcp/
  server.py       # FastMCP server, tool registration
  client.py       # SlackClient with 4 transport methods
  tools/          # 35 modules, one per API family
```

The client supports four transport modes to handle the full spectrum of Slack's API surface:

| Method | Encoding | Auth | Use case |
|--------|----------|------|----------|
| `api_call` | Form | xoxp | Standard Web API |
| `api_call_json` | JSON | xoxp | Endpoints with nested objects (canvases, lists) |
| `session_call` | JSON | xoxc+xoxd | Undocumented endpoints |
| `session_call_form` | Form | xoxc+xoxd | Legacy undocumented endpoints |

## Tests

```sh
# Unit tests (mocked, no tokens needed)
uv run pytest tests/

# Integration tests (requires valid tokens in .env)
uv run pytest tests/ -m integration
```

257 passing, 56 skipped. Skips are endpoints that require bot tokens, specific OAuth scopes, or Enterprise Grid — not bugs.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
