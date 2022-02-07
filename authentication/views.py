from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings

from authentication.oauth import authorize_url
from request.requests import Request

# Create your views here.


async def user_auth_login(request):
    return JsonResponse({
        "authorize_url": authorize_url,
    })


def oauth_callback(request):
    print(request.GET)
    print(request)
    error = request.GET.get("error", None)
    if error:
        # TODO: Handle error
        ...
    # else:
    #     code = request.GET.get("code", None)
    #     if code:
            
    pass
    