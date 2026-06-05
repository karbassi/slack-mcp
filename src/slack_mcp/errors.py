"""Slack error-code classification.

One home for the Slack error strings that the client, the resolver, and tools
branch on. Each classifier answers a distinct question; the handling (raise,
downgrade to None, retry via session) stays at the call site.
"""

from __future__ import annotations

# Auth/token failures on session (xoxc/xoxd) endpoints — tokens missing,
# expired, or revoked. The client turns these into a helpful re-grab message.
AUTH_ERRORS = frozenset({
    "not_authed",
    "invalid_auth",
    "token_expired",
    "token_revoked",
})

# Benign "the thing isn't there / isn't visible" errors — safe to treat the
# referenced id as simply absent rather than propagating a failure.
NOT_FOUND_ERRORS = frozenset({
    "user_not_found",
    "user_not_visible",
    "channel_not_found",
    "bot_not_found",
})


def is_auth_failure(error: str | None) -> bool:
    """The call failed because session tokens are missing/expired/revoked."""
    return error in AUTH_ERRORS


def is_not_found(error: str | None) -> bool:
    """The referenced user/channel/bot doesn't exist or isn't visible."""
    return error in NOT_FOUND_ERRORS


def is_missing_scope(error: str | None) -> bool:
    """The official token lacks a scope the method requires (often retryable
    via the session endpoint)."""
    return error == "missing_scope"
