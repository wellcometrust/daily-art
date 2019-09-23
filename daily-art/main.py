import random

import requests

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from .resources.data import get_data, convert_iiif_width, ArtWork
from .resources.slack_hook import SlackHook

works = get_data()

app = FastAPI(title="Random Wellcome Art", port=8000)
app.mount("/static", StaticFiles(directory="daily-art/static"),
          name="static")
templates = Jinja2Templates(directory="daily-art/templates")


def get_random_artwork(width):
    """ Utility function to get random artwork """
    idx = random.randint(0, len(works) - 1)

    works[idx]["full_image_uri"] = convert_iiif_width(
        works[idx]["full_image_uri"], width=width
    )

    return works[idx]


@app.get("/random-art")
def random_art(request: Request, width: int = 400):
    """ Returns a rendered web page with a random artwork """
    work = get_random_artwork(width=width)

    return templates.TemplateResponse(
        "main.html", {"work": work, "request": request}
    )


@app.get("/random-art/json", response_model=ArtWork)
def random_art_json(width: int = 400):
    """ Returns a json with a random artwork"""
    work = get_random_artwork(width=width)

    return work


@app.post("/random-art/slack")
def random_art_slack(hook: SlackHook, width: int=400):
    """ Posts a random artwork to a given slack hook """
    work = get_random_artwork(width=width)

    slack_json = SlackHook.convert_to_work_slack_post(work)
    requests.post(hook.link, json=slack_json)

    return work