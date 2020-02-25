import requests


def get_visually_similar_artworks(work_id: str, n: int = 3):
    """ Returns a list of `n` visually similar artworks """
    url = f"https://labs.wellcomecollection.org/feature-similarity/works/{work_id}?n={n}"
    similarity_req = requests.get(url)

    if similarity_req:
        return [similarity_api_result_to_similar_work(n) for n in similarity_req.json()["neighbours"]]
    else:
        return []


def get_title(work_id: str):
    url = f"https://api.wellcomecollection.org/catalogue/v2/works/{work_id}"
    work_req = requests.get(url)

    if url:
        return work_req.json()["title"]
    else:
        return ""


def similarity_api_result_to_similar_work(neighbour):
    """ Converts results from the similarity API to the model used in daily-art """
    return {
        "id": neighbour["catalogue_id"],
        "title": get_title(neighbour["catalogue_id"]),
        "full_image_uri": neighbour["miro_uri"],
        "collection_url": neighbour["catalogue_uri"]
    }
