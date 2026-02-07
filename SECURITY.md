# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly via [GitHub's private vulnerability reporting](https://github.com/karbassi/slack-mcp/security/advisories/new).

Do **not** open a public issue for security vulnerabilities.

## Token Handling

This project works with sensitive Slack credentials:

- **`SLACK_XOXP_TOKEN`** — User OAuth token with broad workspace access
- **`SLACK_XOXC_TOKEN`** / **`SLACK_XOXD_TOKEN`** — Browser session tokens for undocumented endpoints

If you believe tokens could be exposed through this project's code (e.g., logged, leaked in errors, or transmitted insecurely), please report it immediately using the method above.

### Best practices

- Never commit tokens to version control
- Use environment variables or a `.env` file (already in `.gitignore`)
- Restrict OAuth scopes to only what you need when creating your Slack app
- Rotate tokens if you suspect they've been compromised
