import os

from slack_mcp.server import mcp


def main():
    # stdio by default; set SLACK_MCP_TRANSPORT=http to run one shared server.
    # Host/Origin checks come from FastMCP's FASTMCP_HTTP_* settings.
    transport = os.environ.get("SLACK_MCP_TRANSPORT", "stdio")
    if transport == "stdio":
        mcp.run()
        return
    if transport != "http":
        msg = f"SLACK_MCP_TRANSPORT must be 'stdio' or 'http', got {transport!r}"
        raise SystemExit(msg)
    mcp.run(
        transport="http",
        host=os.environ.get("SLACK_MCP_HOST", "127.0.0.1"),
        port=int(os.environ.get("SLACK_MCP_PORT", "8501")),
        show_banner=False,
    )


if __name__ == "__main__":
    main()
