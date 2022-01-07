import requests
from requests_oauthlib import OAuth1

from django.views import View
from django.http import JsonResponse
from django.conf import settings

from request.api import Api
from request.requests import Request


# Create your views here.

BASE_URL = settings.TWITTER_API_BASE_URL
BASE_URL_V1 = settings.TWITTER_API_BASE_URL_V1


class GetUserByUsername(View):
    def get(self, request, username):
        endpoint = Api.get_user_by_username(username)
        params = {
            "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities",
            "expansions": "pinned_tweet_id",
            "tweet.fields": "attachments,context_annotations,created_at,entities,geo,in_reply_to_user_id,lang,public_metrics,reply_settings,source",
        }
        options = {
            "params": params,
        }
        response = Request.make(endpoint, options)
        return JsonResponse(response)


# TODO: Add endpoint for user tweets


class GetUserTweetById(View):
    def get(self, request, id):
        endpoint = Api.get_user_tweets_by_id(id)
        params = {
            "tweet.fields": "attachments,context_annotations,created_at,entities,geo,in_reply_to_user_id,lang,public_metrics,reply_settings,source",
            "expansions": "author_id,attachments.media_keys",
            "user.fields": "created_at,pinned_tweet_id,verified",
            "max_results": 5,
        }
        options = {
            "params": params,
        }
        response = Request.make(endpoint, options)
        return JsonResponse(response)


class SearchUserByQuery(View):
    def get(self, request):
        endpoint = Api.search_users()
        params = {
            "q": request.GET.get("q"),
        }
        options = {
            "params": params,
        }
        response = Request.make(endpoint, options)
        print(response)
        return JsonResponse(response, safe=False)


class UserShow(View):
    def get(self, request):
        endpoint = Api.users_show()
        params = {}
        if "user_id" in request.GET:
            params["user_id"] = request.GET.get("user_id")
        else:
            params["screen_name"] = request.GET.get("screen_name")
        options = {
            "params": params,
        }
        response = Request.make(endpoint, options)
        return JsonResponse(response)
