"""Tests for Slack error-code classification."""

from slack_mcp.errors import (
    AUTH_ERRORS,
    NOT_FOUND_ERRORS,
    is_auth_failure,
    is_missing_scope,
    is_not_found,
)


class TestIsAuthFailure:
    def test_matches_auth_errors(self):
        assert all(is_auth_failure(e) for e in AUTH_ERRORS)

    def test_rejects_others(self):
        assert not is_auth_failure("channel_not_found")
        assert not is_auth_failure("missing_scope")
        assert not is_auth_failure(None)


class TestIsNotFound:
    def test_matches_not_found_errors(self):
        assert all(is_not_found(e) for e in NOT_FOUND_ERRORS)

    def test_rejects_others(self):
        assert not is_not_found("invalid_auth")
        assert not is_not_found(None)


class TestIsMissingScope:
    def test_matches(self):
        assert is_missing_scope("missing_scope")

    def test_rejects_others(self):
        assert not is_missing_scope("channel_not_found")
        assert not is_missing_scope(None)


def test_sets_are_disjoint():
    assert not (AUTH_ERRORS & NOT_FOUND_ERRORS)
