# Explicit per-method tool functions over generated tools

**Status:** accepted

We expose ~218 Slack API methods as hand-written `@mcp.tool` functions, one per
method, grouped one file per API family. FastMCP offers machinery that could
generate these instead — `Tool.from_tool` + `ArgTransform`, tool factories, and
an experimental OpenAPI parser that builds tools from a spec. We deliberately do
**not** use it: an explicit function per method is the project's core
navigability contract. You can grep `chat_post_message` and land on the exact
function, its parameters, its docstring, and its tests. A generator would trade
that for a `(method, params)` table or spec indirection, which is far less
legible to both humans and the LLM agents that drive this server — the opposite
of the project's stated goal.

## Considered options

- **Generate tools from a table / OpenAPI spec (rejected).** Less boilerplate,
  but the boilerplate is the point: each forwarder is a discoverable, testable,
  individually-documented unit. Generation also fights the "one tool per method,
  one file per family" convention recorded in CLAUDE.md.
- **Explicit functions + shared depth in the client (accepted).** Keep the
  forwarders explicit; push genuinely shared behaviour *below* the FastMCP tool
  boundary into `SlackClient`. The None-dropping refactor (omitting absent
  optional kwargs in `SlackClient`, so tools forward arguments unconditionally)
  is the model: it removed ~115 copies of the `if x is not None` idiom without
  touching a single tool signature or schema.

## Consequence

The repetition across tool *signatures* is accepted as the cost of
navigability. Cross-cutting concerns are deepened in the client and in FastMCP
middleware (caching, name resolution, response compaction) — never by collapsing
the explicit tool surface.
