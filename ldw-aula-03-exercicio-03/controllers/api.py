import requests

FAMILIES_API = "https://68c853475d8d9f5147350c80.mockapi.io/api/sylvanian-families/families"
CHARACTERS_API = "https://68c853475d8d9f5147350c80.mockapi.io/api/sylvanian-families/characters"


def get_families():
    resp = requests.get(FAMILIES_API)
    resp.raise_for_status()
    return resp.json()


def post_family(data):
    resp = requests.post(FAMILIES_API, json=data)
    resp.raise_for_status()
    return resp.json()


def get_characters():
    resp = requests.get(CHARACTERS_API)
    resp.raise_for_status()
    return resp.json()


def post_character(data):
    resp = requests.post(CHARACTERS_API, json=data)
    resp.raise_for_status()
    return resp.json()
