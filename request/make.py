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
