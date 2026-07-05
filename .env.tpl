SLACK_XOXP_TOKEN={{ op://vault/item/xoxp }}
SLACK_XOXC_TOKEN={{ op://vault/item/xoxc }}
SLACK_XOXD_TOKEN={{ op://vault/item/xoxd }}
# Integration tests refuse to run unless auth.test resolves to this team ID —
# the seatbelt against mutating a real workspace. Set to the throwaway test
# workspace's team ID (T…, from auth.test).
SLACK_TEST_TEAM_ID={{ op://vault/item/test_team_id }}
