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

import hashlib
import hmac
import json

import requests

import config

SIG_HDR = 'X-Hub-Signature'


def handle(event, context):
    """
    Entry point of AWS Lambda.
    event: dictionary containing, among other things, body text
    context: lambda related info...
    """
    # Verify signature
    if SIG_HDR not in event['headers']:
        print('ERROR: No signature found.')
        return
    hexdigest = event['headers'][SIG_HDR]
    digest = hmac.new(config.LOVE_SECRET, event['body'], hashlib.sha1)
    if hexdigest != digest.hexdigest():
        print('ERROR: Signature verification failed.')
        return

    # Now deliver webhook to Slack
    text = (': ' + data['message']) if config.INCLUDE_MESSAGE else ' :heart:'
    data = json.loads(event['body'])
    message = (
        '<{base_url}/explore?user={sender_username}|{sender_name}> loved '
        '<{base_url}/explore?user={receiver_username}|{receiver_name}>{text}'
    ).format(
        base_url=config.LOVE_BASE_URL,
        sender_username=data['sender']['username'],
        sender_name=data['sender']['full_name'],
        receiver_username=data['receiver']['username'],
        receiver_name=data['receiver']['full_name'],
        text=text,
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
