import requests

from django.views import View
from django.http import JsonResponse
from django.conf import settings

from request.endpoints import ENDPOINTS
from request.headers import REQUEST_HEADER
from request import make


# Create your views here.

BASE_URL = settings.TWITTER_API_BASE_URL


class GetUserByUsername(View):
    def get(self, request, username):
        url = BASE_URL + ENDPOINTS["FETCH_SINGLE_USER_BY_USERNAME"] + username
        params = {
            "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified",
        }
        response = requests.request(
            method="GET", url=url, headers=REQUEST_HEADER, params=params
        )
        return JsonResponse(response.json())
