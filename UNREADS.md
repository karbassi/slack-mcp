# Slack MCP Server: Unread Messages Support

## Problem

The current Slack MCP server (`korotovsky/slack-mcp-server@1.1.28`) has no way to get unread messages. It exposes `conversations_history`, `conversations_search_messages`, `conversations_replies`, `channels_list`, and `conversations_add_message` — but nothing for unreads.

## What we discovered

**The Slack API has no single "get unreads" endpoint.** Here's what exists:

| Approach | Token | Speed | Works? |
|---|---|---|---|
| `client.counts` | `xoxc` + `d` cookie | 1 API call, returns all unread channels/DMs/MPIMs with counts | **Yes** — tested and confirmed |
| `conversations.info` per channel (check `last_read` vs latest msg) | `xoxp` | 2 calls per channel (~400 calls for 200 channels) | Works but slow |
| `conversations.info` `unread_count` field | `xoxp` | 1 call per channel | Returns `null` with xoxp tokens |

**`client.counts` is the winner.** One call, returns structured data:

```json
{
  "channels": [{"id": "C...", "has_unreads": true, "mention_count": 3, "latest": "..."}],
  "mpims": [...],
  "ims": [...]
}
```

## Auth requirements

The MCP server needs **two tokens**:

- **`xoxc`** — session token (starts with `xoxc-`), used as Bearer token
- **`xoxd`** — the `d` cookie value (starts with `xoxd-`), sent as `Cookie: d=...` header

Both are stored in 1Password: `op://homelab/Slack API Tokens/xoxc-token` and `op://homelab/Slack API Tokens/xoxd-token`. These tokens last ~1 year (tied to Slack's `d` cookie expiry).

The existing `xoxp` token can still be used for non-session endpoints (search, history, posting).

## Suggested MCP tools for a new server

1. **`get_unreads`** — calls `client.counts`, returns unread DMs/MPIMs/channels with mention counts
2. **`get_unread_messages`** — given a channel ID, fetches messages since `last_read`
3. **`mark_read`** — calls `conversations.mark` to mark a conversation as read
4. **`conversations_history`** — existing functionality
5. **`conversations_search`** — existing functionality
6. **`send_message`** — post to channel/thread
7. **`channels_list`** — existing functionality

## Key API calls

```bash
# Get all unreads (xoxc required)
curl -s "https://slack.com/api/client.counts" \
  -H "Authorization: Bearer $XOXC" \
  -H "Cookie: d=$XOXD" \
  -d "token=$XOXC"

# Mark as read (xoxp works)
curl -s "https://slack.com/api/conversations.mark" \
  -H "Authorization: Bearer $XOXP" \
  -d "channel=C123&ts=1234567890.123456"
```

## Reference

- [korotovsky PR #171](https://github.com/korotovsky/slack-mcp-server/pull/171) — attempted to add unreads but uses the slow xoxp approach
- `client.counts` is undocumented but stable — it's what the Slack client itself uses
- 1Password item ID for tokens: `iq5rz6hbhd3g2sgn3wfd72z27y`
