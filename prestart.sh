#! /usr/bin/env bash

python daily-art/resources/data.py

if [[ "$SLACK_HOOK" != "" ]]; then
    cat /app/cronspecs.txt | crontab
    cron
fi
