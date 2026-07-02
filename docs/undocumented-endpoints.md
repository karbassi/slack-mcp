# Undocumented Slack endpoints

Captured by driving the Slack web client (`app.slack.com`) for the **Slack MCP** test workspace through Chrome DevTools while a `fetch`/`XHR` interceptor logged every `/api/` and `/cache/` call, then probing each live with the workspace `xoxc`/`xoxd` tokens. 101 distinct endpoints observed across boot, Today, Home, Files, Later, DMs, Activity, a channel, channel-details, member list, a profile, and search.

Endpoints that were already wrapped when this catalog was first written are omitted from the tables below (see "Already wrapped" at the bottom). The Tier 1 and Tier 2 tables are kept for reference and are now marked wrapped — their endpoints also appear under "Already wrapped". All probes ran against the live test workspace; "Returns" lists the top-level response keys.

> **Snapshot captured 2026-07.** Slack's undocumented endpoints change without notice — re-probe an endpoint (see "How to reproduce") to confirm its args and response shape before wrapping it.

## Tier 1 — ✅ wrapped (PR #80, issue #58)

_All six now shipped as MCP tools; the code docstrings are the source of truth for args._


| Endpoint | Args | Returns | Tool idea |
| --- | --- | --- | --- |
| `subscriptions.thread.getView` | `limit`, `priority_mode`, `fetch_threads_state` | `threads`, `total_unread_replies`, `new_threads_count`, `has_more`, `max_ts` | List my threads + unread reply counts |
| `activity.feed` | **form-encoded.** Required: `mode` (only `chrono_v1` is valid), `types` (comma-separated). Optional: `limit`, `unread_only`, `priority_only`, `archive_only`, `is_activity_inbox` | `items` (mentions, reactions, replies, reminders, DM bundles, invites) | "What needs my attention" |
| `ai.alpha.summarize.unreadsSnapshot` | — | `summary` | Summarize my unreads |
| `client.dms` | `count`, `exclude_bots`, `include_channel`, `include_closed`, `priority_mode` | `ims`, `mpims` | List my DMs / group DMs |
| `lists.getMyItems` | `include_approvals`, `include_subtasks` | `lists`, `records`, `counts` | My Slack List tasks |
| `saved.get` | `items` — each requires `item_id`, `item_type`, `ts`, and `item_detail` (string, may be empty) | saved-item details | Pairs with existing `saved.list` |

## Tier 2 — ✅ wrapped (PRs #81–#93, issue #59)

_All shipped as MCP tools; code docstrings are the source of truth. Corrections found during implementation (vs the original capture) are called out below._

| Endpoint | Args | Returns |
| --- | --- | --- |
| `connectInvites.list` | `invite_types` (enum-string list; Slack rejects unknown values — vocab undetermined), `only_pending_invites` | `connect_invites` |
| `conversations.teamConnections` | **form-encoded.** `channel` (required) | `connections`, `pending_connections`, `previous_connections` |
| `files.getShares` | `file_id` | `conversation_shares`, `file_channel_shares`, `tab_shares`, `viewer_count` (omitted when unshared) |
| `files.recentlyDeleted` | — | `files` |
| `files.favorites.list` | `type` (**required**, not optional) | favorited files |
| `functions.workflows.list` | `limit`, `filter_options`, `sort_options`, `workflow_builder_only` | `workflows`, `workflow_triggers` |
| `workflows.triggers.list` | `app_ids` | `triggers`, `rejected_triggers` |
| `today.items.list` | — | `items`, `is_generating_focus_topics` — **feature-gated: returns `unknown_method` where the Today view isn't rolled out** |
| `ai.alpha.digest.list` | — | `digests`, `is_stale_or_empty_digest` |
| `users.customStatus.list` | `statuses_count_per_section` | `statuses`, `scheduled_statuses` |
| `users.profile.getExtras` | `user` (optional; defaults to caller), `keys` | `channels`, `shared_channels`, `full_member_channels`, `onboarding_complete` |
| `users.profile.getSections` | **form-encoded.** `user` (required) | profile sections under key **`result`** (not `sections`) |
| `calendar.getInstalledCalendars` | — | `gcal`, `ocal` |
| `calendar.user.status` | — | `status` |
| `lists.templates` | — | `templates`, `starter_templates`, `template_files` |
| `lists.records.list` | `list_id` (required), `archived`, `include_subtasks`, `include_suggested` | list records |
| `canvases.getCannedTemplates` | — | `files` |
| `enterpriseSearch.getConnectors` | — | `connectors` |
| `conversations.suggestions` | — | `status`, `suggestion_types_tried` |
| `search.inline` | **form-encoded.** `query`, `count`, `channel`/`user` (exactly one required) | inline search results |
| `search.save` | `terms`, `type` | saves a search (write) |

## Write actions (driven live in the test workspace; params confirmed)

Sent a message, reacted, pinned, saved-for-later, and deleted it while capturing request bodies. The project's write coverage is already solid — every action below is wrapped, and the real client params match what we send:

| Endpoint | Observed params |
| --- | --- |
| `chat.postMessage` | `channel`, `ts` (client-generated), `blocks` (rich_text), `client_msg_id`, `draft_id`, `client_context_team_id`, `unfurl`, `include_channel_perm_error` |
| `chat.delete` | `channel`, `ts` |
| `reactions.add` | `channel`, `timestamp`, `name` |
| `pins.add` | `channel`, `timestamp` |
| `saved.add` | `item_type`, `item_id`, `ts` |

New read endpoints surfaced while interacting (confirmed `ok: true`):

| Endpoint | Args | Returns |
| --- | --- | --- |
| `subscriptions.thread.get` | `channel`, `thread_ts` | `subscriptions` (single-thread state; complements wrapped `getView`/`mark`) |
| `emoji.collections.list` | `installed_only` | `available`, `installed` (emoji packs) |
| `conversations.bulkReacjiTriggers` | `channel_ids` | `channel_triggers` |

Edge: `emojis/list` (on `edgeapi`) also fires when the emoji picker opens.

## Tier 3 — skip (infra / telemetry / enterprise-config noise)

`activity.views`, `client.extras`, `client.shouldReload`, `enterprise.prefs.get`, `feature.usage.info`, `features.access.policies.list`, `help.issues.ticketStats`, `helpdesk.get`, `megaphone.notifications.list`, `onboarding.fetch`, `onboarding.updateUser`, `payments.status.get`, `quip.lookupThreadIds`, `search.autocomplete`, `search.precache`, `sfdc.integration.listOrgs`, `sharedInvites.canGetLink`, `slackbot.mcp.list`, `team.targetingCriteria`, `ublockworkaround.history`, `users.stateMachine`, `users.interactions.list`/`set` (required args not determined), `admin.roles.entity.listAssignments`, `ai.alpha.translate.locales`, `team.slackConnectGuidelines.get`

## Edge cache API (`edgeapi.slack.com/cache/{team_id}/…`)

A separate fast-lookup host the client uses heavily. Different host and payload shape than `session_call`, so it would need a new client method (e.g. `edge_call`). Observed: `channels/search`, `users/search`, `users/list`, `users/info`, `users/counts`, `channels/info`, `channels/membership`, `huddles/list`, `huddles/info`, `permissions/info`. The standouts are `channels/search` and `users/search` — fuzzy server-side search without the official `search.*` OAuth scopes.

Common args: `enterprise_token` (required on enterprise grids), plus per-endpoint `query`, `fuzz`, `count`, `filter`, `updated_ids`.

## Already wrapped (captured and confirmed live)

`aiApps.list`, `api.features`, `bookmarks.list`, `client.counts`, `client.userBoot`, `conversations.history`, `conversations.listPrefs`, `conversations.mark`, `conversations.view`, `dnd.info`, `dnd.teamInfo`, `drafts.list`, `experiments.getByUser`, `files.info`, `files.list`, `messages.list`, `saved.list`, `search.modules.channels`, `search.modules.dms`, `search.modules.files`, `search.modules.messages`, `search.modules.people`, `team.info`, `team.profile.get`, `users.channelSections.list`, `users.prefs.get`, `users.prefs.set`, `users.priority.list`, `users.profile.get`

Tier 1 (PR #80): `subscriptions.thread.getView`, `activity.feed`, `ai.alpha.summarize.unreadsSnapshot`, `client.dms`, `lists.getMyItems`, `saved.get`

Tier 2 (PRs #81–#93): `emoji.collections.list`, `lists.templates`, `lists.records.list`, `calendar.getInstalledCalendars`, `calendar.user.status`, `canvases.getCannedTemplates`, `files.getShares`, `files.recentlyDeleted`, `files.favorites.list`, `functions.workflows.list`, `workflows.triggers.list`, `users.profile.getExtras`, `users.profile.getSections`, `users.customStatus.list`, `today.items.list`, `conversations.teamConnections`, `conversations.suggestions`, `conversations.bulkReacjiTriggers`, `ai.alpha.digest.list`, `connectInvites.list`, `subscriptions.thread.get`, `search.inline`, `search.save`, `enterpriseSearch.getConnectors`

## How to reproduce

1. Log a Chrome instance into the test workspace (or inject the `xoxd` value as a non-httpOnly `d` cookie on `.slack.com`).
2. Install a `fetch`/`XHR` interceptor (via DevTools `initScript`) that records `method name + non-`token`/non-`_x_` form fields` into `localStorage`.
3. Click through every surface; the interceptor dedupes by endpoint and merges observed arg names.
4. Probe each candidate with `curl -F token=$XOXC -H "Cookie: d=$XOXD"` to confirm `ok` and response keys.
</content>
</invoke>
