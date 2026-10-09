import pytest

from slack_mcp import __main__ as entry


@pytest.fixture
def run_calls(monkeypatch):
    calls = []
    monkeypatch.setattr(entry.mcp, "run", lambda *a, **kw: calls.append((a, kw)))
    for var in ("SLACK_MCP_TRANSPORT", "SLACK_MCP_HOST", "SLACK_MCP_PORT"):
        monkeypatch.delenv(var, raising=False)
    return calls


def test_defaults_to_stdio(run_calls):
    entry.main()
    assert run_calls == [((), {})]


def test_http_defaults_to_loopback(monkeypatch, run_calls):
    monkeypatch.setenv("SLACK_MCP_TRANSPORT", "http")
    entry.main()
    assert run_calls == [
        ((), {"transport": "http", "host": "127.0.0.1", "port": 8501, "show_banner": False})
    ]


def test_http_host_and_port_from_env(monkeypatch, run_calls):
    monkeypatch.setenv("SLACK_MCP_TRANSPORT", "http")
    monkeypatch.setenv("SLACK_MCP_HOST", "0.0.0.0")
    monkeypatch.setenv("SLACK_MCP_PORT", "9000")
    entry.main()
    assert run_calls[0][1]["host"] == "0.0.0.0"
    assert run_calls[0][1]["port"] == 9000


def test_rejects_unknown_transport(monkeypatch, run_calls):
    monkeypatch.setenv("SLACK_MCP_TRANSPORT", "sse")
    with pytest.raises(SystemExit):
        entry.main()
    assert run_calls == []
