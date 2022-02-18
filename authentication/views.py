from distutils.log import error
from urllib.parse import parse_qs

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from authentication import oauth

from authentication.oauth import OAuth
from request.requests import Request
from authentication.models import AccessToken

oauth_session = None


def oauth_request_token(request):
    try:
        global oauth_session
        oauth_session = OAuth()
        response = oauth_session.get_request_token()
        oauth_token = response["oauth_token"]
        authorize_url = oauth_session.make_authorize_url(oauth_token)
        return JsonResponse({
            "authorize_url": authorize_url,
        })
    except Exception as e:
        return JsonResponse({"error": e})


# TODO: Fix database entry error, authentication_token has no column named oauth_token
def user_auth_login(request, token, verifier):
    try:
        if oauth_session is not None:
            previous_oauth_token = oauth_session.get_oauth_token()
        if token == previous_oauth_token:
            tokens = oauth_session.get_access_token(token, verifier)
            oauth_token = tokens["oauth_token"][0]
            oauth_token_secret = tokens["oauth_token_secret"][0]
            user_id = tokens["user_id"][0]
            token, created = AccessToken.objects.get_or_create(
                oauth_token=oauth_token,
                oauth_token_secret=oauth_token_secret,
                user_id=user_id,
            )
            jwt = oauth_session.encode_token({
                "user_id": user_id
            })
            return JsonResponse({
                "token": jwt,
            })
        else:
            return JsonResponse({
                "error": "Invalid credentials",
                "code": 401,
            },
            status=401)
    except Exception as e:
        return JsonResponse({"error": e.message})


# def user_auth_login(request, token, verifier):
#     try:
#         oauth_token = request.GET.get("oauth_token", None)
#         oauth_verifier = request.GET.get("oauth_verifier", None)
#         if oauth_session is not None:
#             previous_oauth_token = oauth_session.get_oauth_token()
#         if oauth_token == previous_oauth_token:
#             tokens = oauth_session.get_access_token(oauth_token, oauth_verifier)
#             oauth_token = tokens["oauth_token"][0]
#             oauth_token_secret = tokens["oauth_token_secret"][0]
#             user_id = tokens["user_id"][0]
#             token, created = AccessToken.objects.get_or_create(
#                 oauth_token=oauth_token,
#                 oauth_token_secret=oauth_token_secret,
#                 user_id=user_id,
#             )
#             return JsonResponse({
#                 "user_token": token.oauth_token,
#             })
#         else:
#             return JsonResponse({
#                 "error": "Invalid credentials",
#                 "code": 401,
#             }, status=401)
#     except Exception as e:
#         return JsonResponse({"error": e.message})
