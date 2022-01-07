import requests

from django.http import JsonResponse
from django.conf import settings

options = {
    "method": "GET",
    "url": "",
    "params": {},
    "data": "",
    "headers": "",
    "timeout": (5,10),
}

BASE_URL = settings.TWITTER_API_BASE_URL


# def make(options=options):
#     for (k, v) in options.items():
#         options[k] = v
#         pass
#     print(options)
#     BASE_URL = settings.TWITTER_API_BASE_URL
#     url = BASE_URL + ENDPOINTS["FETCH_SINGLE_USER_BY_USERNAME"] + options["username"]
#     params = {
#         "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified",
#     }
#     response = requests.get(url, headers=REQUEST_HEADER, params=params)
#     return JsonResponse(response.json())
