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
WELLCOME_DATASET_URL = "https://data.wellcomecollection.org/" \
                         "catalogue/v2/works.json.gz"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArtWork(BaseModel):
    id: str
    title: str
    description: str
    full_image_uri: str
    collection_url: str
    contributors: List


def convert_iiif_width(uri, width="full"):
    """ Utility to convert IIIF to image URI with given width or "full" """
    uri_end = uri.split("//")[1].split("/")
    uri_end[4] = ("full" if width == "full" else str(width) + ",")

    return "https://" + "/".join(uri_end)


def get_data(exclude_used=False):
    """ Gets data from the collection webpage or cached file """
    logger.info("Recovering dataset.")
    try:
        f = open(join(LOCAL_PATH_TO_DATA, FILTERED_FILENAME), 'r')
    except FileNotFoundError:
        logger.info("Cache not found, downloading dataset from source.")
        works = download_data_from_source()
    else:
        logger.info("Hit cache! Loading from local file.")
        works = json.load(f)

        works = {
            idx: work for idx, work in works.items()
            if not work.get('used') or not exclude_used
        }

        f.close()

    logger.info("Finished loading {} filtered art works.".format(len(works)))
    return works


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
    with open(join(LOCAL_PATH_TO_DATA, FILTERED_FILENAME), 'w') as f:
        json.dump({work['id']: work for work in works}, f)

    return works


if __name__ == "__main__":
    works = get_data()
