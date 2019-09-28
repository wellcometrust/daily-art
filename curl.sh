#!/bin/bash

curl --request POST \
  --url http://127.0.0.1:8000/random-art/slack \
  --header 'content-type: application/json' \
  --data '{
	"link": "SLACK_HOOK"
  }'
