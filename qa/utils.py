import requests


def api_get(url):
    res = requests.get(url)
    if res:
        return res.json()
    else:
        return None


def api_post(url, data):
    res = requests.post(url, data=data)
    if res:
        return res.json()
    else:
        return None



