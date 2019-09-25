import random
import requests

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse

from .resources.data import ArtWork, get_data, update_data, convert_iiif_width

from .resources.slack_hook import SlackHook

app = FastAPI(title="Random Wellcome Art", port=8000)
app.mount("/static", StaticFiles(directory="daily-art/static"),
          name="static")
templates = Jinja2Templates(directory="daily-art/templates")


def get_random_artwork(width, exclude_used=False, exclude_sensitive=False):
    """ Utility function to get random artwork """
    filtered_works = get_data(
        exclude_used=exclude_used, exclude_sensitive=exclude_sensitive
    )

    idx = random.randint(0, len(filtered_works) - 1)
    work_id = list(filtered_works.keys())[idx]

    filtered_works[work_id]["full_image_uri"] = convert_iiif_width(
        filtered_works[work_id]["full_image_uri"], width=width
    )

    if exclude_used:
        update_data(work_id, used=True)

    return filtered_works[work_id]


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
def random_art_slack(hook: SlackHook, width: int = 600):
    """ Posts a random artwork to a given slack hook """
    work = get_random_artwork(width=width,
                              exclude_used=True,
                              exclude_sensitive=True)

    slack_json = SlackHook.convert_to_work_slack_post(work)
    requests.post(hook.link, json=slack_json)

    return work


@app.get("/flag/{work_id}")
def flag_art(work_id: str, sensitivity: bool = False, redirect: bool = False):
    """ Flags art as sensitive or not """

    update_data(work_id=work_id, sensitivity=sensitivity)

    if redirect:
        return RedirectResponse("/random-art")
    else:
        return {"message": "Work id {} correctly updated".format(work_id)}
