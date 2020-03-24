import os
import logging
import requests

import csv
import random

from resources.data import get_data, save_data_locally

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def consolidate_with_history(path_already_presented, exclude_sensitive=True,
                             only_interesting=True, save=False):
    """
    Utility function to exclude a list of images from the app. Useful to
    consolidate with history for different deployments.

    Args:
        path_already_presented: A path to a csv file with every line containing
        a work_id

        exclude_sensitive: whether to exclude sensitive works
        only_interesting: whether to only show images marked as "interesting"
        save: Whether to save the result, replacing the current local json,
        as defined in resources.data

    Returns:

    """

    filtered_works = get_data(
        exclude_sensitive=exclude_sensitive,
        only_interesting=only_interesting
    )
    work_keys = list(filtered_works.keys())
    random.shuffle(work_keys)

    filtered_works = {
        key: filtered_works[key]
        for key in work_keys
    }

    with open(os.path.join(SCRIPT_PATH, path_already_presented),
              'r') as f:
        reader = csv.reader(f)
        presented = [row[0] for row in reader]

    for work in filtered_works.values():
        work["used"] = False

    for work_id in presented:
        filtered_works[work_id]["used"] = True

    filtered_works = {idx: work for idx, work in filtered_works.items() if
                      not work['used']}

    logger.info(f"Final number of works: {len(filtered_works)}")
    if save:
        logger.info("Saving filtered file locally. Replaces any existing file")
        save_data_locally(filtered_works)

    return filtered_works


def refresh_local_file(host="localhost", port=8000, protocol="http"):
    """ Queries the API annotations and saves the local file """
    works = requests.get(f"{protocol}://{host}:{port}/works").json()
    save_data_locally(works)


