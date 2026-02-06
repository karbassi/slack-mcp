# Slack Web API Methods Report — User Token (`xoxp-*`) Scope

Target: MCP server supporting **user token (`xoxp-*`) only**. Admin tokens (`xoxp-...` with admin scopes) and bot tokens (`xoxb-*`) are excluded.

## Included Method Families (177 methods, 31 families)

| Family | Count |
|---|---|
| `conversations.*` | 28 |
| `files.*` | 16 |
| `chat.*` | 13 |
| `users.*` | 12 |
| `slackLists.*` (lists) | 12 |
| `team.*` | 9 |
| `apps.*` | 8 |
| `workflows.*` | 7 |
| `usergroups.*` | 7 |
| `canvases.*` | 6 |
| `calls.*` | 6 |
| `reminders.*` | 5 |
| `dnd.*` | 5 |
| `views.*` | 4 |
| `reactions.*` | 4 |
| `bookmarks.*` | 4 |
| `stars.*` | 3 |
| `search.*` | 3 |
| `pins.*` | 3 |
| `oauth.*` | 3 |
| `auth.*` | 3 |
| `assistant.*` | 3 |
| `rtm.*` | 2 |
| `openid.*` | 2 |
| `functions.*` | 2 |
| `tooling.*` | 1 |
| `migration.*` | 1 |
| `entity.*` | 1 |
| `emoji.*` | 1 |
| `dialog.*` | 1 |
| `bots.*` | 1 |
| `api.*` | 1 |

## Excluded

| Excluded Family | Count | Reason |
|---|---|---|
| `admin.*` | 98 | Requires admin/org-level token |
| `channels.*` | 15 | Deprecated (use `conversations.*`) |
| `groups.*` | 16 | Deprecated (use `conversations.*`) |
| `im.*` | 6 | Deprecated (use `conversations.*`) |
| `mpim.*` | 6 | Deprecated (use `conversations.*`) |

**Total excluded:** 141 methods

## All 177 Methods

### api (1)
- `api.test`

### apps (8)
- `apps.connections.open`
- `apps.event.authorizations.list`
- `apps.manifest.create`
- `apps.manifest.delete`
- `apps.manifest.export`
- `apps.manifest.update`
- `apps.manifest.validate`
- `apps.uninstall`

### assistant (3)
- `assistant.threads.setStatus`
- `assistant.threads.setSuggestedPrompts`
- `assistant.threads.setTitle`

### auth (3)
- `auth.revoke`
- `auth.teams.list`
- `auth.test`

### bookmarks (4)
- `bookmarks.add`
- `bookmarks.edit`
- `bookmarks.list`
- `bookmarks.remove`

### bots (1)
- `bots.info`

### calls (6)
- `calls.add`
- `calls.end`
- `calls.info`
- `calls.participants.add`
- `calls.participants.remove`
- `calls.update`

### canvases (6)
- `canvases.access.delete`
- `canvases.access.set`
- `canvases.create`
- `canvases.delete`
- `canvases.edit`
- `canvases.sections.lookup`

### chat (13)
- `chat.appendStream`
- `chat.delete`
- `chat.deleteScheduledMessage`
- `chat.getPermalink`
- `chat.meMessage`
- `chat.postEphemeral`
- `chat.postMessage`
- `chat.scheduleMessage`
- `chat.scheduledMessages.list`
- `chat.startStream`
- `chat.stopStream`
- `chat.unfurl`
- `chat.update`

### conversations (28)
- `conversations.acceptSharedInvite`
- `conversations.approveSharedInvite`
- `conversations.archive`
- `conversations.canvases.create`
- `conversations.close`
- `conversations.create`
- `conversations.declineSharedInvite`
- `conversations.externalInvitePermissions.set`
- `conversations.history`
- `conversations.info`
- `conversations.invite`
- `conversations.inviteShared`
- `conversations.join`
- `conversations.kick`
- `conversations.leave`
- `conversations.list`
- `conversations.listConnectInvites`
- `conversations.mark`
- `conversations.members`
- `conversations.open`
- `conversations.rename`
- `conversations.replies`
- `conversations.requestSharedInvite.approve`
- `conversations.requestSharedInvite.deny`
- `conversations.requestSharedInvite.list`
- `conversations.setPurpose`
- `conversations.setTopic`
- `conversations.unarchive`

### dialog (1)
- `dialog.open`

### dnd (5)
- `dnd.endDnd`
- `dnd.endSnooze`
- `dnd.info`
- `dnd.setSnooze`
- `dnd.teamInfo`

### emoji (1)
- `emoji.list`

### entity (1)
- `entity.presentDetails`

### files (16)
- `files.comments.delete`
- `files.completeUploadExternal`
- `files.delete`
- `files.getUploadURLExternal`
- `files.info`
- `files.list`
- `files.remote.add`
- `files.remote.info`
- `files.remote.list`
- `files.remote.remove`
- `files.remote.share`
- `files.remote.update`
- `files.revokePublicURL`
- `files.sharedPublicURL`
- `files.upload`
- `files.upload.v2`

### functions (2)
- `functions.completeError`
- `functions.completeSuccess`

### migration (1)
- `migration.exchange`

### oauth (3)
- `oauth.access`
- `oauth.v2.access`
- `oauth.v2.exchange`

### openid (2)
- `openid.connect.token`
- `openid.connect.userInfo`

### pins (3)
- `pins.add`
- `pins.list`
- `pins.remove`

### reactions (4)
- `reactions.add`
- `reactions.get`
- `reactions.list`
- `reactions.remove`

### reminders (5)
- `reminders.add`
- `reminders.complete`
- `reminders.delete`
- `reminders.info`
- `reminders.list`

### rtm (2)
- `rtm.connect`
- `rtm.start`

### search (3)
- `search.all`
- `search.files`
- `search.messages`

### slackLists (12)
- `slackLists.access.delete`
- `slackLists.access.set`
- `slackLists.create`
- `slackLists.download.get`
- `slackLists.download.start`
- `slackLists.items.create`
- `slackLists.items.delete`
- `slackLists.items.deleteMultiple`
- `slackLists.items.info`
- `slackLists.items.list`
- `slackLists.items.update`
- `slackLists.update`

### stars (3)
- `stars.add`
- `stars.list`
- `stars.remove`

### team (9)
- `team.accessLogs`
- `team.billableInfo`
- `team.billing.info`
- `team.externalTeams.disconnect`
- `team.externalTeams.list`
- `team.info`
- `team.integrationLogs`
- `team.preferences.list`
- `team.profile.get`

### tooling (1)
- `tooling.tokens.rotate`

### usergroups (7)
- `usergroups.create`
- `usergroups.disable`
- `usergroups.enable`
- `usergroups.list`
- `usergroups.update`
- `usergroups.users.list`
- `usergroups.users.update`

### users (12)
- `users.conversations`
- `users.deletePhoto`
- `users.discoverableContacts.lookup`
- `users.getPresence`
- `users.identity`
- `users.info`
- `users.list`
- `users.lookupByEmail`
- `users.profile.get`
- `users.profile.set`
- `users.setPhoto`
- `users.setPresence`

### views (4)
- `views.open`
- `views.publish`
- `views.push`
- `views.update`

### workflows (7)
- `workflows.featured.add`
- `workflows.featured.list`
- `workflows.featured.remove`
- `workflows.featured.set`
- `workflows.stepCompleted`
- `workflows.stepFailed`
- `workflows.updateStep`

## Sources

- [Slack Web API Methods Reference](https://docs.slack.dev/reference/methods/)
- [Slack Python SDK source (legacy_client.py)](https://github.com/slackapi/python-slack-sdk/blob/main/slack_sdk/web/legacy_client.py)
- [Slack OpenAPI Specs](https://github.com/slackapi/slack-api-specs)
