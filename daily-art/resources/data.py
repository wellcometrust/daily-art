import json
import logging
import requests
import gzip

from os.path import abspath, dirname, join
from os import remove

from pydantic import BaseModel
from typing import List

LOCAL_PATH_TO_DATA = join(
    abspath(dirname(__file__)),
    '../../data'
)
FILTERED_FILENAME = 'filtered_list_of_works.json'

# Wellcome_DATASET_URL contains the entire list of works
# S3_DATASET contains a subset, already filtered by description and
# pre-annotated.

WELLCOME_DATASET_URL = "https://data.wellcomecollection.org/" \
                       "catalogue/v2/works.json.gz"

S3_DATASET_URL = "https://wellcome-collection-data.s3.eu-west-2" \
                 ".amazonaws.com/annotated-data/filtered_list_of_works.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimilarWork(BaseModel):
    id: str
    title: str
    full_image_uri: str
    collection_url: str


class ArtWork(BaseModel):
    id: str
    title: str
    description: str
    full_image_uri: str
    collection_url: str
    contributors: List
    similar_works: List[SimilarWork]


def convert_iiif_width(uri, width="full"):
    """ Utility to convert IIIF to image URI with given width or "full" """
    uri_end = uri.split("//")[1].split("/")
    uri_end[4] = ("full" if width == "full" else str(width) + ",")

    return "https://" + "/".join(uri_end)


def get_data(exclude_used=False,
             exclude_sensitive=False,
             only_interesting=True):
    """
    Gets data from the cached file, if it fails, downloads from the s3 bucket,
    and if the s3 bucket fails, downloads from the Wellcome Collection API.

    Args:
        exclude_used: whether to exclude works with the key "used"
        exclude_sensitive: whether to exclude works with the key "sensitivity"

    Returns: dict of works

    """
    logger.info("Recovering dataset.")
    try:
        with open(join(LOCAL_PATH_TO_DATA, FILTERED_FILENAME), 'r') as f:
            works = json.load(f)
            logger.info("Hit cache! Loading from local file.")
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        logger.info("Cache not loaded, downloading dataset from S3.")
        try:
            works = download_data_from_annotated_s3_bucket()
        except:
            logger.info("Could not connect to S3 bucket. "
                        "Downloading dataset from Wellcome API URI")
            works = download_data_from_source()

    works = {
        idx: work for idx, work in works.items()
        if (not work.get('used') or not exclude_used) and
           (not work.get('sensitivity') or not exclude_sensitive) and
           (work.get('interesting') or not only_interesting)
    }

    if not exclude_used:
        for id in works.keys():
            works[id]["used"] = False

    logger.info("Finished loading {} filtered art works.".format(len(works)))
    return works


def update_data(work_id, **kwargs):
    """ Update json file with boolean kwargs from false to true. """
    logger.info("Updating data")
    try:
        f = open(join(LOCAL_PATH_TO_DATA, FILTERED_FILENAME), 'r')
        works = json.load(f)
        f.close()
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        logger.info("File not loaded, downloading data first.")
        works = get_data()
    finally:
        logging.info("Work {} updated with {}".format(work_id, kwargs))

        for key, value in kwargs.items():
            if not works[work_id].get(key):
                works[work_id][key] = value

        save_data_locally(works)


def download_data_from_annotated_s3_bucket():
    """ Gets annotated data, pre-filtered and with annotated sensitivity """

    works = requests.get(S3_DATASET_URL).json()

    save_data_locally(works)

    return works


def save_data_locally(works):
    """ Saves a json with works locally"""

    with open(join(LOCAL_PATH_TO_DATA, FILTERED_FILENAME), 'w') as f:
        json.dump(works, f)


def download_data_from_source():
    """ Downloads data from Wellcome API """
    counter = 0

    filtered_list_of_works = []

    # Filters artwork that has description with length in [min_len, max_len]
    min_len = 200
    max_len = 2000

    logger.info("Downloading data.")
    dataset_content = requests.get(WELLCOME_DATASET_URL).content

    logger.info("Saving tmp files.")
    tmp_file = join(LOCAL_PATH_TO_DATA, 'works.json.gz')
    with open(tmp_file, 'wb') as f:
        f.write(dataset_content)

    logger.info("Unzipping file and reading raw content.")
    for line in gzip.open(tmp_file, 'rb'):
        if counter % 100000 == 0:
            logger.info("Processing work number {}".format(counter))

        import pdb
        pdb.set_trace()
        counter += 1

        json_line = json.loads(line.decode('utf-8'))

        if json_line.get("thumbnail") and json_line["thumbnail"].get("url") \
                and json_line.get("description") \
                and json_line.get("contributors") \
                and min_len < len(json_line.get("description")) < max_len:
            filtered_list_of_works += [json_line]

    filtered_list_of_works = sorted(filtered_list_of_works,
                                    key=lambda x: len(x['description']),
                                    reverse=True)

    works = [
        {
            "id": work["id"],
            "title": work["title"],
            "description": work["description"],
            "full_image_uri": convert_iiif_width(work["thumbnail"]["url"]),
            "collection_url": "https://wellcomecollection.org/works/" +
                              work["id"],
            "contributors": work["contributors"]
        }
        for work in filtered_list_of_works
    ]

    logger.info("Removing tmp file.")
    remove(tmp_file)

    # Converts to dictionary indexed by id for O(1) acesss
    works = {work['id']: work for work in works}

    with open(join(LOCAL_PATH_TO_DATA, FILTERED_FILENAME), 'w') as f:
        json.dump(works, f)

    return works


if __name__ == "__main__":
    get_data()
    #download_data_from_source()
