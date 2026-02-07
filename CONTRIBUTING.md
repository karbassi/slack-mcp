# Contributing

Thanks for your interest in contributing to Slack MCP.

## Setup

```sh
git clone https://github.com/karbassi/slack-mcp.git
cd slack-mcp
uv sync
```

## Development

### Code style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

```sh
# Check for lint errors
uv run ruff check .

# Auto-fix lint errors
uv run ruff check . --fix

# Format code
uv run ruff format .

# Check formatting without changing files
uv run ruff format . --check
```

### Running tests

```sh
# Unit tests (mocked, no tokens needed)
uv run pytest tests/

# Integration tests (requires SLACK_XOXP_TOKEN in .env)
uv run pytest tests/ -m integration
```

### Adding a new tool

Each Slack API family has its own module in `src/slack_mcp/tools/`. To add a new tool:

1. Find (or create) the module for the API family in `src/slack_mcp/tools/`
2. Add the tool function following the existing pattern:

```python
from typing import Optional

from fastmcp.dependencies import Depends

from slack_mcp.server import mcp, slack_client
from slack_mcp.client import SlackClient


@mcp.tool
async def family_method_name(
    required_param: str,
    optional_param: Optional[str] = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Short description of what this method does."""
    kwargs = {"required_param": required_param}
    if optional_param is not None:
        kwargs["optional_param"] = optional_param
    return await client.api_call("family.methodName", **kwargs)
```

3. If you created a new module, register it in `src/slack_mcp/server.py`:

```python
import slack_mcp.tools.your_module
```

4. Add tests in `tests/test_tools/`:
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
