import os

import csv
import random

from resources.data import get_data

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

def consolidate_with_history():
    filtered_works = get_data(
        exclude_sensitive=True, only_interesting=True
    )
    work_keys = list(filtered_works.keys())
    random.shuffle(work_keys)

    filtered_works = {
        key: filtered_works[key]
        for key in work_keys
    }

    with open(os.path.join(SCRIPT_PATH, '../data/already_presented.csv'),
              'r') as f:
        reader = csv.reader(f)

        presented = [row[4].split('/')[-1] for row in reader]

    for work in filtered_works.values():
        work["used"] = False

    for work_id in presented:
        filtered_works[work_id]["used"] = True

    return {idx: work for idx, work in filtered_works.items() if
            not work['used']}


