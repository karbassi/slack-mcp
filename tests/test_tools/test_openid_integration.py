import pytest

from slack_mcp.tools.openid import (
    openid_connect_token,
    openid_connect_user_info,
)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a valid OIDC authorization code")
async def test_openid_connect_token_live(live_client):
    pass


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skip(reason="requires a token from OIDC flow")
async def test_openid_connect_user_info_live(live_client):
    pass
