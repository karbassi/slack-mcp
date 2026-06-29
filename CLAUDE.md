# CLAUDE.md

## Commands

```bash
mise run test              # unit tests
mise run test:integration  # integration tests (requires .env tokens)
mise run lint              # ruff linter
mise run typecheck         # ty type checker
mise run security          # semgrep security + AI best practices + custom rules
mise run check             # all checks (test + lint + typecheck + security)
```

## Testing

- Run integration tests after adding or modifying any tool
- Tokens for the test workspace ("Slack MCP") live in `.env`
- Tests that need a channel must create a temp channel and archive it after — see `temp_channel` fixture in `test_chat_integration.py`
- ~68 integration tests are skipped — these require a bot token (xoxb), Slack Connect, interactive triggers, or would be destructive. Adding a bot token is a future TODO

## Code Layout

```
src/slack_mcp/
├── server.py        # FastMCP app, caching + name resolution middleware
├── client.py        # SlackClient — api_call, session_call, session_call_form, session_call_multipart
└── tools/           # One file per API family, @mcp.tool decorated
    ├── undocumented.py  # Session-only endpoints (xoxc/xoxd)
    ├── legacy.py        # Undocumented endpoints for existing API families
    └── *.py             # Official Slack Web API methods
```

## Conventions

- One tool per Slack API method, one file per API family
- Official methods use `client.api_call`; undocumented use `client.session_call`
- Unit tests in `tests/test_tools/test_<family>.py`, integration in `test_<family>_integration.py`
- `admin.*` endpoints are intentionally excluded

## Known Quirks

- Draft `client_last_updated_ts` must be 7 decimal places — use `_pad_draft_ts()`
- `session_call_form` must include `charset=utf-8` in Content-Type to avoid `missing_charset` warnings

## Agent skills

### Issue tracker

Issues and PRDs are tracked as GitHub issues in `karbassi/slack-mcp` via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical triage roles, default strings (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
