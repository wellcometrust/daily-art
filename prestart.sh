#! /usr/bin/env bash

python daily-art/resources/data.py

cat /app/cronspecs.txt | crontab
cron
