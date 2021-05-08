import requests


def get_visually_similar_artworks(work_id: str, n: int = 3):
    """ Returns a list of `n` visually similar artworks """
    url = f"https://api.wellcomecollection.org/catalogue/v2/images/{work_id}?include=visuallySimilar"
    similarity_req = requests.get(url)

    if similarity_req:
        return [similarity_api_result_to_similar_work(n) for n in similarity_req.json()["visuallySimilar"]]
    else:
        return []


def get_title(work_id: str):
    url = f"https://api.wellcomecollection.org/catalogue/v2/works/{work_id}"
    work_req = requests.get(url)

    if url:
        return work_req.json()["title"]
    else:
        return ""


def convert_iiif_info_to_image_uri(uri):
    return uri.replace('info.json', '') + 'full/max/0/default.jpg'


def similarity_api_result_to_similar_work(neighbour):
    """ Converts results from the similarity API to the model used in daily-art """
    return {
        "id": neighbour['source']['id'],
        "title": neighbour['source']['title'],
        "full_image_uri": convert_iiif_info_to_image_uri(neighbour['thumbnail']['url']),
        "collection_url": f"https://wellcomecollection.org/works/{neighbour['source']['id']}"
    }
