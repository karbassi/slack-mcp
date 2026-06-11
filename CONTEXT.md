# Slack MCP

A FastMCP server that exposes Slack's API as MCP tools — one tool per Slack method — with a middleware stack that resolves IDs to names, compacts bulky responses, caches reads, and flags Slack errors.

## Language

### Tools & API surface

**Tool**:
One MCP-exposed function wrapping exactly one Slack API method.
_Avoid_: command, endpoint, handler

**Tool family**:
The single file grouping all Tools for one Slack API namespace (e.g. `conversations.py`).
_Avoid_: module, category, package

**Official method**:
A documented Slack Web API method, called through `SlackClient.api_call` with the xoxp token.
_Avoid_: public API, REST method

**Undocumented endpoint**:
A Slack session-only endpoint with no public docs, called through `SlackClient.session_call*` with session tokens.
_Avoid_: private API, hidden/internal endpoint

**Legacy endpoint**:
An Undocumented endpoint that backs an existing Official method family (lives in `legacy.py`).
_Avoid_: deprecated method

### The Slack boundary

**SlackClient**:
The single adapter to Slack — exposes `api_call`/`api_call_json` (official, form/JSON) and `session_call`/`session_call_form`/`session_call_multipart` (undocumented, session auth).
_Avoid_: SDK, connection, the API

**Session tokens**:
The xoxc + xoxd browser credentials that authorize Undocumented endpoints.
_Avoid_: cookies, browser auth

**Session fallback**:
A Tool retrying an Official method as an Undocumented endpoint when Slack returns `missing_scope` (e.g. `conversations_mark`).
_Avoid_: retry, downgrade

### The middleware stack

**Middleware stack**:
The ordered chain every Tool call passes through: Error flagging → Response cache → Thread cache → Name resolution → Compaction → Tool.
_Avoid_: pipeline, chain, interceptors

**Error flagging**:
Marking a Slack `ok:false` response as an MCP error by setting `ToolResult.is_error` (outermost, so it survives a cache hit).
_Avoid_: error handling, validation

**Response cache**:
Per-Tool caching of read results, keyed by arguments, with a TTL declared at the Tool via `meta={"cache_ttl": ...}`.
_Avoid_: memoization

**Thread cache**:
Caching of old-message reads — `conversations_replies` and bounded `conversations_history` — keyed on timestamps older than an hour.
_Avoid_: message cache

**Name resolution**:
Enriching a response with human names for the user/channel/bot IDs it contains, added under `resolved_names`.
_Avoid_: lookup, hydration, enrichment

**Compaction**:
Stripping bulky fields from a Slack response unless `detailed` is set; a Tool opts in with `@compactable`.
_Avoid_: trimming, minifying, filtering

**detailed**:
A per-Tool argument that bypasses Compaction to return the full Slack response.
_Avoid_: verbose, raw

**skip-resolution**:
A Tool tag that opts the Tool out of Name resolution.
_Avoid_: no-resolve

## Relationships

- A **Tool** belongs to exactly one **Tool family** and wraps exactly one Slack method.
- Every **Tool** call passes through the **Middleware stack** in order, then reaches the **SlackClient**.
- **Error flagging** is outermost so `is_error` is recomputed from the response even on a **Response cache** hit (the cache wrapper drops the flag).
- A **Response cache** or **Thread cache** hit short-circuits **Name resolution** and **Compaction**.
- **Compaction** runs only when the Tool is `@compactable` and **detailed** is not set.
- **Name resolution** runs unless the Tool carries the **skip-resolution** tag.
- A **Tool** uses an **Official method** by default and may use **Session fallback** to an **Undocumented endpoint**.

## Example dialogue

> **Dev:** "If `conversations_history` is a cache hit, does the response still get **Name resolution**?"
> **Maintainer:** "No — a **Response cache** hit short-circuits the inner middleware, so the cached value already has `resolved_names` baked in. But **Error flagging** still runs, because it sits outside the cache and re-derives `is_error` from the response."
> **Dev:** "And if Slack returns `ok:false` on an **Undocumented endpoint**?"
> **Maintainer:** "**Error flagging** sets `is_error`. Official methods never reach it as `ok:false` — the SDK raises first."

## Flagged ambiguities

- **"client"** was used for two distinct things: the server-side **SlackClient** (our adapter to Slack) and the MCP-protocol `Client` (an LLM-side caller, also used as the in-memory test harness). Resolved: **SlackClient** always means the Slack adapter; **Client** (capitalized, unqualified) means the MCP client.
- **"cache"** spans three caches: the **Response cache**, the **Thread cache**, and the resolver's own disk cache backing **Name resolution**. Always qualify which.
