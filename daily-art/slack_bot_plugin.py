""" A plug-in to the API to schedule slack messages without cron """
import os
import requests

from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
from dateutil.tz import tzutc
from datetime import datetime

from resources.data import get_data
from data_consolidate_plugin import consolidate_with_history

API_HOST = os.environ.get('API_HOST', "http://127.0.0.1:8000")
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

import random

filtered_works = consolidate_with_history(path_already_presented=
                                          '../data/already_presented.csv')

work_keys = list(filtered_works.keys())
random.shuffle(work_keys)

filtered_works = {
    key: filtered_works[key]
    for key in work_keys
}

with open('ad_hoc.csv', 'r') as f:
    work_ids = [work.split(',')[1] for work in f.read().splitlines()]

print(len(filtered_works))

if __name__ == "__main__":

    dt_1970 = datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())

    start_date = datetime(2020, 2, 12, 10, 00, tzinfo=tzutc())
    end_date = datetime(2020, 4, 11, 10, 00, tzinfo=tzutc())

    generated_messages = []

    f = open('data_list.csv', 'w')
    i = 0
    for date in rrule(DAILY,
                      dtstart=start_date,
                      until=end_date,
                      byweekday=(MO, TU, WE, TH, FR)):
        unix_time = int((date - dt_1970).total_seconds())
        post_data = {
            "token": BOT_TOKEN,
            "link": "https://slack.com/api/chat.scheduleMessage",
            "channel_id": CHANNEL_ID,
            "post_at": unix_time
        }
        work_id = work_ids[i]
        i += 1

        work_query = "?work_id={}".format(work_id)

        r = requests.post(
            API_HOST + "/random-art/slack" + work_query,
            json=post_data
        )

        message_json = r.json()
        scheduled_message_id = message_json['scheduled_message_id']
        generated_messages += [scheduled_message_id]

        csv_line = \
            f"{date},"\
            f"{work_id},"\
            f"{scheduled_message_id},"\
            f"{unix_time},"\
            f"{message_json['message']['attachments'][0]['title_link']}\n"

        f.write(csv_line)
        print(csv_line, end='')

    f.close()
