# Ralph Prompt: Slack MCP Server

## Goal

Build a FastMCP 3.0 MCP server that exposes ALL Slack Web API methods (listed in `methods.txt`) as MCP tools, using user tokens only. Each method gets its own tool with typed parameters, unit tests, and integration tests.

## Context Files

Read these before starting:

- `TECH_STACK.md` — tech stack decisions
- `methods.txt` — all 178 official methods + undocumented methods
- `manifest.json` — Slack app manifest with 44 user token scopes
- `TODO.md` — progress tracker (create if missing, update as you go)

## Important: Use context7 for documentation

The `context7` plugin is installed. Use it to look up library docs before writing code.

Context7 library IDs (use these directly, do not search):
- **FastMCP 3.0** — `/jlowin/fastmcp/v3.0.0b1` — tools, `Depends()`, server setup
- **slack-sdk** — `/slackapi/python-slack-sdk` — `AsyncWebClient`, `api_call`, method parameters, response types
- **pytest** — `/pytest-dev/pytest` — fixtures, markers, test patterns
- **pytest-asyncio** — `/pytest-dev/pytest-asyncio` — async test setup
- **httpx** — `/encode/httpx` — async HTTP client for undocumented endpoints
- **respx** — `/lundberg/respx` — mocking httpx requests in tests
- **python-dotenv** — `/theskumar/python-dotenv` — loading `.env` files

FastMCP 3.0 is beta so the API may differ from what you expect. Always check docs first.

Do NOT guess at library APIs. Do NOT fetch web pages manually. Use context7.

## TODO.md

On first run, generate `TODO.md` from `methods.txt`. Include **every single method** — do not abbreviate with `...` or ellipsis. Format:

```markdown
# TODO

## Phase 1: Scaffolding
- [ ] pyproject.toml + uv sync
- [ ] .env.tpl / .gitignore / op inject
- [ ] src/slack_mcp/client.py
- [ ] src/slack_mcp/server.py
- [ ] tests/conftest.py

## Phase 2: Official API Tools
- [ ] api.test
- [ ] apps.connections.open
- [ ] apps.event.authorizations.list
- [ ] apps.manifest.create
(... list ALL 178 methods from methods.txt lines 1-178, one per line ...)
- [ ] workflows.updateStep

## Phase 3: Undocumented Session Endpoints
- [ ] client.boot
- [ ] client.counts
- [ ] client.userBoot
- [ ] threads.getView

## Phase 4: Undocumented Legacy Endpoints
- [ ] bots.list
- [ ] channels.delete
- [ ] chat.command
- [ ] commands.list
- [ ] files.edit
- [ ] files.share
- [ ] team.prefs.get
- [ ] users.admin.invite
- [ ] users.admin.setInactive
- [ ] users.prefs.get
- [ ] users.prefs.set
```

**At each iteration**, read `TODO.md` to find the next unchecked item. After completing a method (tool + unit test + integration test + commit), mark it `[x]` and commit the TODO update with the tool commit.

## Phase 1: Project Scaffolding

Set up the project structure before implementing any tools.

1. Initialize `pyproject.toml` with uv, Python 3.13:
   - dependencies: `fastmcp>=3.0.0b1`, `slack-sdk`, `httpx`, `python-dotenv`
   - dev dependencies: `pytest`, `pytest-asyncio`, `respx` (for mocking httpx)
   - Add `[tool.pytest.ini_options]` with `markers = ["integration: real Slack API tests"]` and `asyncio_mode = "auto"`
2. Run `uv sync` to create venv and install all dependencies
3. Create `.env.tpl` with 1Password references:
   ```
   SLACK_XOXP_TOKEN={{ op://homelab/Test Slack/xoxp }}
   SLACK_XOXC_TOKEN={{ op://homelab/Test Slack/xoxc }}
   SLACK_XOXD_TOKEN={{ op://homelab/Test Slack/xoxd }}
   ```
4. Run `op inject -f -i .env.tpl -o .env` to generate `.env` with real tokens (use `-f` to overwrite if exists)
5. `.gitignore` is already created — verify `.env` is listed
6. Create `src/slack_mcp/__init__.py`
7. Create `src/slack_mcp/client.py` — a `SlackClient` class that:
   - Calls `load_dotenv()` from `python-dotenv` to load `.env` on import
   - Reads tokens from environment variables: `SLACK_XOXP_TOKEN`, `SLACK_XOXC_TOKEN`, `SLACK_XOXD_TOKEN`
   - Initializes `slack_sdk.web.async_client.AsyncWebClient` with the `xoxp` token
   - Initializes `httpx.AsyncClient` for undocumented endpoints with `xoxc` + `xoxd` cookie
   - Exposes `api_call(method, **kwargs)` for official methods
   - Exposes `session_call(method, **kwargs)` for undocumented methods
   - Is a singleton or module-level instance so it's created once, not per tool call
8. Create `src/slack_mcp/server.py` — FastMCP server entry point that:
   - Calls `load_dotenv()` at startup before anything else
   - Creates the `FastMCP` instance
   - Creates a `SlackClient` dependency using `Depends()` so tools receive it via injection
   - Imports all tool modules
9. Create `src/slack_mcp/__main__.py` so the server can run via `uv run python -m slack_mcp`
10. Create `tests/conftest.py` with shared fixtures:
   - `mock_client` — mocked SlackClient for unit tests
   - `live_client` — real SlackClient from `.env` for integration tests; use `pytest.importorskip` or `pytest.mark.skipif(not os.getenv("SLACK_XOXP_TOKEN"))` to skip if env vars missing
11. Generate `TODO.md` from `methods.txt` — list every method, no abbreviations
12. Verify: `uv run pytest` passes with 0 tests collected (no errors)
13. Commit: `feat: scaffold project structure with FastMCP 3.0 and Slack client`

## Phase 2: Implement Tools — One API at a Time

Work through `TODO.md` **top to bottom, one unchecked item at a time**. For each method:

### For each official API method:

1. Read `TODO.md`, find the next unchecked method
2. Look up the method's parameters using context7 (slack-sdk docs) or the installed `slack_sdk` source
3. Create or append to the appropriate tool module in `src/slack_mcp/tools/{family}.py`
4. Define the tool as an async function decorated with `@mcp.tool` with:
   - Typed parameters matching the Slack API (use `Optional` for optional params)
   - `client: SlackClient` injected via `Depends()` — do NOT instantiate SlackClient inside the tool
   - Clear docstring describing what the method does
   - Calls `client.api_call()` with the method name and parameters
   - Returns the API response
5. Write a **unit test** in `tests/test_tools/test_{family}.py` that:
   - Mocks the Slack API response
   - Calls the tool with the mocked client
   - Asserts the correct API method was called with correct parameters
   - Asserts the response is returned correctly
6. Write an **integration test** in `tests/test_tools/test_{family}_integration.py` that:
   - Uses the `live_client` fixture (from `.env`)
   - Calls the real Slack API against the sandbox workspace
   - For read-only methods: asserts `response["ok"] is True`
   - For destructive methods: see "Destructive Method Testing" section below
   - Marked with `@pytest.mark.integration`
7. Run `uv run pytest tests/test_tools/test_{family}.py -x` — unit tests must pass
8. Mark the method `[x]` in `TODO.md`
9. Commit: `feat(tools): add {method_name} tool`
10. Move to the next unchecked item in `TODO.md`

### Destructive Method Testing

Some methods mutate state (archive channels, delete files, kick users, etc.). For integration tests of destructive methods:

- **Create-then-destroy pattern**: If testing `conversations.archive`, first create a temp channel, then archive it, then clean up.
- **Assert the API accepted the call**: Check `response["ok"] is True` or that the expected error code is returned (e.g., `channel_not_found` if testing with a known-bad ID).
- **Never run destructive methods against existing sandbox data**. Always create test data first.
- **If a destructive test is too risky** (e.g., `apps.uninstall`), write the integration test but mark it `@pytest.mark.skip(reason="destructive: would uninstall the app")` and note it in `TODO.md`.

### Tool naming convention

Convert Slack method names to snake_case for the tool function name:
- `chat.postMessage` → `chat_post_message`
- `conversations.history` → `conversations_history`
- `files.upload.v2` → `files_upload_v2`
- `slackLists.items.create` → `slack_lists_items_create`

### Tool module file mapping

Group tools by the first segment of the method name:
- `api.*` → `src/slack_mcp/tools/api.py`
- `apps.*` → `src/slack_mcp/tools/apps.py`
- `assistant.*` → `src/slack_mcp/tools/assistant.py`
- `auth.*` → `src/slack_mcp/tools/auth.py`
- `bookmarks.*` → `src/slack_mcp/tools/bookmarks.py`
- `bots.*` → `src/slack_mcp/tools/bots.py`
- `calls.*` → `src/slack_mcp/tools/calls.py`
- `canvases.*` → `src/slack_mcp/tools/canvases.py`
- `chat.*` → `src/slack_mcp/tools/chat.py`
- `conversations.*` → `src/slack_mcp/tools/conversations.py`
- `dialog.*` → `src/slack_mcp/tools/dialog.py`
- `dnd.*` → `src/slack_mcp/tools/dnd.py`
- `emoji.*` → `src/slack_mcp/tools/emoji.py`
- `entity.*` → `src/slack_mcp/tools/entity.py`
- `files.*` → `src/slack_mcp/tools/files.py`
- `functions.*` → `src/slack_mcp/tools/functions.py`
- `migration.*` → `src/slack_mcp/tools/migration.py`
- `oauth.*` → `src/slack_mcp/tools/oauth.py`
- `openid.*` → `src/slack_mcp/tools/openid.py`
- `pins.*` → `src/slack_mcp/tools/pins.py`
- `reactions.*` → `src/slack_mcp/tools/reactions.py`
- `reminders.*` → `src/slack_mcp/tools/reminders.py`
- `rtm.*` → `src/slack_mcp/tools/rtm.py`
- `search.*` → `src/slack_mcp/tools/search.py`
- `slackLists.*` → `src/slack_mcp/tools/slack_lists.py`
- `stars.*` → `src/slack_mcp/tools/stars.py`
- `team.*` → `src/slack_mcp/tools/team.py`
- `tooling.*` → `src/slack_mcp/tools/tooling.py`
- `usergroups.*` → `src/slack_mcp/tools/usergroups.py`
- `users.*` → `src/slack_mcp/tools/users.py`
- `views.*` → `src/slack_mcp/tools/views.py`
- `workflows.*` → `src/slack_mcp/tools/workflows.py`

## Phase 3: Undocumented Session Endpoints

After all 178 official methods are done, implement the 4 undocumented session endpoints in `src/slack_mcp/tools/undocumented.py`:

- `client.boot` → `client_boot`
- `client.counts` → `client_counts`
- `client.userBoot` → `client_user_boot`
- `threads.getView` → `threads_get_view`

These use `SlackClient.session_call()` with `xoxc` + `xoxd` auth.

Write unit + integration tests for each. Integration tests should skip if `SLACK_XOXC_TOKEN` is not set. Commit per method: `feat(tools): add undocumented {method} tool`

## Phase 4: Undocumented Legacy Endpoints

After Phase 3, implement the 11 legacy undocumented methods in `src/slack_mcp/tools/legacy.py`:

- `bots.list`, `channels.delete`, `chat.command`, `commands.list`, `files.edit`, `files.share`, `team.prefs.get`, `users.admin.invite`, `users.admin.setInactive`, `users.prefs.get`, `users.prefs.set`

These are from [ErikKalkoken/slackApiDoc](https://github.com/ErikKalkoken/slackApiDoc). They originally required legacy tokens (which can no longer be created), but may work with `xoxc` + `xoxd` session tokens. Use `SlackClient.session_call()`.

- Write unit tests for each (mocked).
- Write integration tests but mark them `@pytest.mark.skip(reason="legacy: requires legacy token or xoxc, may not work")` unless they actually work against the sandbox.
- Commit per method: `feat(tools): add legacy undocumented {method} tool`

## Completion Criteria

All of the following must be true:

- [ ] Every method in `methods.txt` (178 official + 4 session undocumented + 11 legacy undocumented) has a corresponding MCP tool
- [ ] Every tool has at least one unit test
- [ ] Every tool has at least one integration test (may be skipped for destructive methods)
- [ ] `uv run pytest --ignore=tests/test_tools -x` passes (non-tool tests)
- [ ] `uv run pytest tests/test_tools/ -x --ignore='*_integration*'` passes (unit tests)
- [ ] `uv run pytest -m integration` passes with 0 unexpected failures (skips are OK)
- [ ] Each method was committed individually with conventional commit format
- [ ] All items in `TODO.md` are checked off
- [ ] Server starts without error: `uv run python -m slack_mcp.server`

When ALL criteria are met, output: <promise>COMPLETE</promise>

## Rules

- Do NOT skip methods. Implement every single one from `methods.txt`.
- Do NOT batch commits. One commit per API method.
- Do NOT proceed to the next method if the current method's unit test fails. Fix it first.
- Do NOT instantiate `SlackClient()` inside tool functions. Use the shared instance via `get_client()`.
- Do NOT implement orchestrated/high-level tools (get_unreads, etc.) — that is a separate phase.
- Do NOT modify `methods.txt`, `manifest.json`, or `TECH_STACK.md`.
- Always read `TODO.md` at the start of each iteration to find your place.
- Always update `TODO.md` after completing each method.
- Always run `uv run pytest tests/test_tools/test_{family}.py -x` before committing — unit tests must pass.
- Only run integration tests when confident they won't break sandbox state, or use create-then-destroy pattern.
- Use conventional commits: `feat(tools): add {method_name} tool`, `fix(tools): fix {method_name} test`, `feat: scaffold project structure`
- Keep tool implementations thin — they are wrappers around the Slack API, not business logic.
- If stuck after 5 attempts on the same method, add a `# BLOCKED: {reason}` comment in `TODO.md` and move to the next method.
- If FastMCP imports or APIs don't work as expected, use context7 to look up the correct API before guessing.
- Run `op inject -f -i .env.tpl -o .env` once during scaffolding. Do NOT re-run it every iteration.
- Integration tests hit the real Slack API. Slack rate limits apply (Tier 3 = ~50 req/min). If you get rate limited, add a short sleep between integration test calls or batch integration test runs at the end of a family rather than per-method.
