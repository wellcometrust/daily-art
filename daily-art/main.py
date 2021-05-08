import os
import random
import requests
import logging

from fastapi import FastAPI
from fastapi.logger import logger

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse

from .resources.data import ArtWork, get_data, update_data, convert_iiif_width
from .resources.similarity import get_visually_similar_artworks
from .resources.slack_hook import SlackHook

CHANNEL_ID = 'daily-art-beta'

app = FastAPI(title="Random Wellcome Art", host="0.0.0.0", port=8000)
app.mount("/static", StaticFiles(directory="daily-art/static"),
          name="static")
templates = Jinja2Templates(directory="daily-art/templates")

filtered_works = get_data(
    exclude_sensitive=True, only_interesting=True, exclude_used=False
)

logger.setLevel(logging.INFO)


def get_random_artwork(width):
    """ Utility function to get random artwork """
    non_used_works = {key: value for key, value in filtered_works.items()
                      if not value["used"]}

    logger.info(f"Still {len(non_used_works)} remaining")

    idx = random.randint(0, len(non_used_works) - 1)
    work_id = list(non_used_works.keys())[idx]

    non_used_works[work_id]["full_image_uri"] = convert_iiif_width(
        non_used_works[work_id]["full_image_uri"], width=width
    )
    non_used_works[work_id]["similar_works"] = get_visually_similar_artworks(work_id)

    return non_used_works[work_id]


@app.get("/random-art")
def random_art(request: Request, width: int = 600):
    """ Returns a rendered web page with a random artwork """
    work = get_random_artwork(width=width)

    return templates.TemplateResponse(
        "main.html", {"work": work, "request": request}
    )


@app.get("/random-art/json", response_model=ArtWork)
def random_art_json(width: int = 600):
    """ Returns a json with a random artwork"""
    work = get_random_artwork(width=width)

    return work


@app.post("/random-art/slack")
def random_art_slack(width: int = 600, work_id: str = ""):
    """ Posts a random artwork to a given slack hook """
    if work_id:
        work = filtered_works[work_id]
        work["similar_works"] = get_visually_similar_artworks(work_id)
    else:
        work = get_random_artwork(width=width)

    hook = os.getenv('SLACK_HOOK', '')
    message = SlackHook()
    slack_json = message.convert_to_work_slack_post(work)
    slack_json["channel"] = CHANNEL_ID
    slack_json["token"] = hook

    slack_request = requests.post(hook, json=slack_json)

    if not slack_request:
        return
    else:
        return slack_request


@app.get("/flag/{work_id}")
def flag_art(work_id: str, sensitivity: bool = False,
             interesting: bool = False,
             redirect: bool = False):
    """ Flags art as sensitive or not """

    filtered_works[work_id]["sensitivity"] = sensitivity
    filtered_works[work_id]["interesting"] = interesting
    filtered_works[work_id]["used"] = True

    if redirect:
        return RedirectResponse("/random-art")
    else:
        return {"message": "Work id {} correctly updated".format(work_id)}


@app.get("/works")
def list_of_works():
    """ Gets list of all works currently running in the app"""
    return filtered_works
