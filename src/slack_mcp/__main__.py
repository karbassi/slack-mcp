import os

from slack_mcp.server import mcp

# The HTTP endpoint has no auth: any caller acts with the Slack tokens, so it
# may only listen on loopback. Put an authenticating proxy in front for remote use.
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


def main():
    # stdio by default; set SLACK_MCP_TRANSPORT=http to run one shared server.
    transport = os.environ.get("SLACK_MCP_TRANSPORT", "stdio")
    if transport == "stdio":
        mcp.run()
        return
    if transport != "http":
        msg = f"SLACK_MCP_TRANSPORT must be 'stdio' or 'http', got {transport!r}"
        raise SystemExit(msg)
    host = os.environ.get("SLACK_MCP_HOST", "127.0.0.1")
    if host not in LOOPBACK_HOSTS:
        msg = f"SLACK_MCP_HOST must be a loopback address, got {host!r}"
        raise SystemExit(msg)
    mcp.run(
        transport="http",
        host=host,
        port=int(os.environ.get("SLACK_MCP_PORT", "8501")),
        show_banner=False,
        # FastMCP defaults this off, leaving the server open to DNS rebinding.
        # Extra trusted hosts/origins come from FASTMCP_HTTP_ALLOWED_HOSTS/_ORIGINS.
        host_origin_protection=True,
    )


if __name__ == "__main__":
    main()
