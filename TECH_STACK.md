# Tech Stack

## Runtime

- **Python 3.13**
- **FastMCP 3.0** — MCP server framework

## Dependencies

- **slack_sdk** (`AsyncWebClient`) — official Slack Web API client for 178 documented methods. Provides typed methods, automatic pagination, rate limit retries, and file upload v2 handling.
- **httpx** — async HTTP client for undocumented session endpoints (`client.counts`, `client.boot`, `client.userBoot`, `threads.getView`) that require `xoxc` + `xoxd` cookie auth.

## Auth

- **`xoxp`** (user token) — standard Slack Web API methods via slack_sdk
- **`xoxc`** + **`xoxd`** (session token + cookie) — undocumented endpoints via httpx
- Tokens stored in 1Password ("Test Slack" item in homelab vault)
- `.env.tpl` checked into git as template with `op://` references
- `.env` generated at startup via `op inject`, gitignored
- Server reads tokens from `.env` environment variables: `SLACK_XOXP_TOKEN`, `SLACK_XOXC_TOKEN`, `SLACK_XOXD_TOKEN`

## Testing

- **pytest** + **pytest-asyncio** — test framework
- Unit tests: mocked HTTP responses (no Slack workspace needed)
- Integration tests: real API calls against developer sandbox (`karbassi-slack-mcp.enterprise.slack.com`), marked with `@pytest.mark.integration`

## Packaging

- **uv** — dependency management, virtual environments, lockfile

## Project Structure

```
slack-mcp/
├── manifest.json          # Slack app manifest (44 user token scopes)
├── methods.txt            # All 178 official + undocumented methods
├── pyproject.toml         # Project config and dependencies
├── src/
│   └── slack_mcp/
│       ├── __init__.py
│       ├── server.py      # FastMCP server entry point
│       ├── client.py      # Slack API client (sdk + httpx)
│       └── tools/         # MCP tool definitions by family
│           ├── __init__.py
│           ├── chat.py
│           ├── conversations.py
│           ├── files.py
│           ├── users.py
│           ├── search.py
│           ├── reactions.py
│           ├── ...
│           └── undocumented.py  # client.counts, etc.
└── tests/
    ├── conftest.py
    ├── test_client.py
    └── test_tools/
        ├── test_chat.py
        ├── test_conversations.py
        └── ...
```

## Sandbox

- **Workspace:** karbassi-slack-mcp.enterprise.slack.com
- **1Password item:** "Test Slack" in homelab vault
- Tokens: `xoxp`, `xoxc`, `xoxd`
