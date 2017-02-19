#!/bin/bash
# Usage: ./deploy.sh

# Create zip package.
rm package.zip
zip package.zip love2slack.py config.py
mkdir libs
pip2 install -t libs requests
pushd libs
zip -r ../package.zip *
popd
rm -rf libs

# Set your lambda function's code.
aws lambda update-function-code \
    --function-name Love2slack \
    --zip-file fileb://package.zip
