"""
Configuration for love2slack.  Belongs in config.py once you fill things out.
"""

# Webhook URL for Slack.
SLACK_WEBHOOK_URL = 'paste'

# Username for bot to post as (can be anything).
SLACK_USERNAME = 'Lover'

# Choose an avatar - either an emoji, or a URL. Set one to a string, the other
# to None.
SLACK_ICON_EMOJI = ':revolving_hearts:'
SLACK_ICON_URL = None

# Choose a channel
SLACK_CHANNEL = '#taintedlove'

# Where is your love instance? No trailing slash.
LOVE_BASE_URL = 'https://cwrulove.appspot.com'
