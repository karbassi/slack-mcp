# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Ruff linter/formatter configuration
- CHANGELOG and CONTRIBUTING guide

## [0.1.0] - 2025-05-01

Initial release.

### Added

- 193 tools across 35 Slack API families
- Full Slack Web API coverage: messages, channels, files, search, reactions, pins, stars, reminders, DND, calls, canvases, lists, workflows, user groups, and more
- 4 undocumented session endpoints (`client.boot`, `client.counts`, `client.userBoot`, `threads.getView`)
- 11 legacy undocumented endpoints (`chat.command`, `files.edit`, `bots.list`, etc.)
- SlackClient with 4 transport methods (form/JSON x official/session)
- FastMCP 3.0 integration with dependency injection
- Slack app manifest with all required OAuth scopes
- 313 tests (257 passing, 56 skipped for missing scopes/tokens)
- Unit tests with mocked client for all tool families
- Integration tests against live Slack API
- `uvx` support for zero-install usage
