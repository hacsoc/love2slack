"""
Notify a slack channel about love sent.

A Yelp/love webhook is a JSON encoded POST request. Sample data:

    {
      "sender": {
        "full_name": "Stephen Brennan",
        "username": "smb196",
        "email": "redacted"
      },
      "receiver": {
        "full_name": "Matthew Bentley",
        "username": "mtb89",
        "email": "redacted"
      },
      "message": "Welcome to the lovefest!",
      "timestamp": "2017-02-14 18:30:00"
    }

In fact, webhooks contain a HMAC in the headers, and webhooks are associated
with a secret so that you can verify them. Unfortunately, headers are not very
simple to receive in AWS Lambda (for some reason...), and so verification is
not currently supported. In the future, yes.
"""

import json

import requests

import config


def handle(event, context):
    """
    Entry point of AWS Lambda.
    event: dictionary containing, among other things, body text
    context: lambda related info...
    """
    data = json.loads(event['body'])
    message = (
        '<{base_url}/explore?user={sender_username}|{sender_name}> loved '
        '<{base_url}/explore?user={receiver_username}|{receiver_name}>: '
        '{message}'
    ).format(
        base_url=config.LOVE_BASE_URL,
        sender_username=data['sender']['username'],
        sender_name=data['sender']['full_name'],
        receiver_username=data['receiver']['username'],
        receiver_name=data['receiver']['full_name'],
        message=data['message'],
    )
    payload = {
        'text': message,
        'username': config.SLACK_USERNAME,
        'channel': config.SLACK_CHANNEL,
    }
    if config.SLACK_ICON_EMOJI:
        payload['icon_emoji'] = config.SLACK_ICON_EMOJI
    elif config.SLACK_ICON_URL:
        payload['icon_url'] = config.SLACK_ICON_URL
    requests.post(config.SLACK_WEBHOOK_URL, json=payload)
