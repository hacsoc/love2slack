love2slack
==========

An AWS Lambda function that takes Yelp Love webhooks and sends them to a Slack
channel.

Setup
-----

Prereqs:
- Yelp love install, and admin account.
- AWS with command line and an appropriate IAM.
- A sane environment that can run a bash script.

Create a webhook on the Slack integration page. Create a `config.py` based on
`config-example.py` and set the webhook URL and any Slack preferences you have.
Make sure to fill out all the variables.

Create an AWS lambda function - give it the name `Love2slack` and make it
Python2.7. Leave it blank, but make sure you specify that the handler is
`love2slack.handle`, and make sure you add an API Gateway trigger with open
security.

Copy the API Gateway URL into the form for creating a Subscription on the Yelp
Love admin pages. Create the Subscription.

Run `./deploy.sh` to deploy your lambda function.

Send love and you should see a message pop up in slack.
