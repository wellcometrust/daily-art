""" A plug-in to the API to schedule slack messages without cron """
import requests

from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
from dateutil.tz import tzutc
from datetime import datetime

from resources.data import get_data

API_HOST = "http://127.0.0.1:8000"
BOT_TOKEN = ""
CHANNEL_ID = ""

import random

filtered_works = get_data(
    exclude_sensitive=True, only_interesting=True
)
work_keys = list(filtered_works.keys())
random.shuffle(work_keys)

filtered_works = {
    key: filtered_works[key]
    for key in work_keys
}

del filtered_works['w38bxm5s']

if __name__ == "__main__":

    dt_1970 = datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())

    start_date = datetime(2019, 9, 30, 10, 00, tzinfo=tzutc())
    end_date = datetime(2020, 2, 22, 10, 00, tzinfo=tzutc())

    generated_messages = []

    for date in rrule(DAILY,
                      dtstart=start_date,
                      until=end_date,
                      byweekday=(MO, TU, WE, TH, FR)):
        post_data = {
            "token": BOT_TOKEN,
            "link": "https://slack.com/api/chat.scheduleMessage",
            "channel_id": CHANNEL_ID,
            "post_at": int((date - dt_1970).total_seconds())
        }
        work_id = filtered_works.popitem()[0]

        work_query = "?work_id={}".format(work_id)
        r = requests.post(API_HOST + "/random-art/slack", json=post_data)

        scheduled_message_id = r.json()['scheduled_message_id']
        generated_messages += [scheduled_message_id]

        print("work_id:{}, message_id:{}".format(work_id, scheduled_message_id))

