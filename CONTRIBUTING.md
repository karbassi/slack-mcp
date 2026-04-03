# Contributing

Thanks for your interest in contributing to Slack MCP.

## Setup

```sh
git clone https://github.com/karbassi/slack-mcp.git
cd slack-mcp
uv sync
```

## Development

### Running checks

```sh
mise run check              # test + lint + security scan
mise run test               # unit tests only
mise run test:integration   # integration tests (requires .env tokens)
mise run lint               # ruff linter
mise run lint:fix           # ruff with auto-fix
mise run security           # semgrep security + custom rules
```

### Code style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, and [Semgrep](https://semgrep.dev/) for security scanning.

```sh
# Format code
uv run ruff format .

# Check formatting without changing files
uv run ruff format . --check
```

### Adding a new tool

Each Slack API family has its own module in `src/slack_mcp/tools/`. To add a new tool:

1. Find (or create) the module for the API family in `src/slack_mcp/tools/`
2. Add the tool function following the existing pattern:

```python
from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def family_method_name(
    required_param: str,
    optional_param: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Short description of what this method does."""
    kwargs = {"required_param": required_param}
    if optional_param is not None:
        kwargs["optional_param"] = optional_param
    return await client.api_call("family.methodName", **kwargs)
```

3. If the tool returns bloated responses (messages with blocks/attachments, files with thumbnails, channel lists), add response compaction:

```python
from slack_mcp.compact import compact_message_list, compactable


@mcp.tool
@compactable(compact_message_list)
async def family_method_name(
    required_param: str,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Short description. Set detailed=True for full response."""
    return await client.api_call("family.methodName", required_param=required_param)
```

Available compactors: `compact_message_list`, `compact_search_messages`, `compact_search_files`, `compact_search_all`, `compact_channel_list`, `compact_file_list`, `compact_single_item`, `compact_items`.

4. If you created a new module, register it in `src/slack_mcp/server.py`:

```python
import slack_mcp.tools.your_module
```

5. Add tests in `tests/test_tools/`:
   - `test_your_module.py` — unit tests using `mock_client`
   - `test_your_module_integration.py` — integration tests using `live_client`

### Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(tools): add new_method tool
fix(client): handle rate limit responses
test(chat): add missing edge case tests
docs: update README with new tool
chore: update dependencies
```

## Reporting issues

Open an issue at [github.com/karbassi/slack-mcp/issues](https://github.com/karbassi/slack-mcp/issues).
