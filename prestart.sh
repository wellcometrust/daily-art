#!/bin/bash

python daily-art/resources/data.py

if [ "$SLACK_HOOK" != "" ]; then
    sed -i /app/curl.sh -e "s@SLACK_HOOK@$SLACK_HOOK@g" /app/curl.sh
    cat /app/cronspecs.txt | crontab -
    cron
fi
