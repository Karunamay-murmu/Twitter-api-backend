import asyncio
from requests_oauthlib import OAuth1

from django.views import View
from django.http import JsonResponse, response
from django.conf import settings

from request.api import Api
from request.requests import Request


# Create your views here.

BASE_URL = settings.TWITTER_API_BASE_URL
BASE_URL_V1 = settings.TWITTER_API_BASE_URL_V1


async def user_by_username(request, username):
    endpoint_v1 = Api.show_user()
    endpoint_v2 = Api.get_user_by_username(username)

    options_v2 = {
        "params": {
            "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
        },
    }
    options_v1 = {
        "params": {
            "screen_name": username,
        },
    }

    response_v1 = await Request.make(endpoint_v1, options_v1)
    response_v2 = await Request.make(endpoint_v2, options_v2)

    if response_v1["status"] == 200 and response_v2["status"] == 200:
        if "pinned_tweet_id" in response_v2["response"]["data"]:
            pinned_tweet_options = {
                "params": {
                    "expansions": "attachments.media_keys",
                    "tweet.fields": "attachments,context_annotations,created_at,entities,geo,in_reply_to_user_id,lang,public_metrics,reply_settings,source",
                    "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
                }
            }
            pinned_tweet_id = response_v2["response"]["data"]["pinned_tweet_id"]
            tweet_endpoint = Api.tweet_lookup(pinned_tweet_id)
            pinned_tweet = await Request.make(tweet_endpoint, pinned_tweet_options)
            response_v2["response"]["pinned_tweet"] = pinned_tweet["response"]
        response_v2["response"]["data"]["profile_banner_url"] = response_v1["response"]["profile_banner_url"]
        return JsonResponse(response_v2["response"], safe=False, status=200)
    return JsonResponse({
        "error": {
            "message": "Error occured while fetching data",
            "status": 500
        }
    }, status=500)


async def user_liked_tweets(request, id):
    url = Api.user_liked_tweets(id)
    options = {
        "params": {
            "tweet.fields": "id,text,attachments,author_id,context_annotations,created_at,entities,in_reply_to_user_id,conversation_id,lang,public_metrics,referenced_tweets,reply_settings,source",
            "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,attachments.media_keys,entities.mentions.username",
            "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
            "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
            "max_results": 10,
        }
    }
    response = await Request.make(url, options)
    if response["status"] == 200:
        return JsonResponse(response["response"], safe=False, status=200)
    return JsonResponse({
        "error": {
            "message": "Error occured while fetching data",
            "status": 500
        }
    }, status=500)


class GetUserTweetById(View):
    def get(self, request, id):
        endpoint_v1 = Api.users_timeline()
        endpoint_v2 = Api.get_user_tweets_by_id(id)
        params_v1 = {
            "tweet_mode": "extended",
            "exclude_replies": "true",
            "trim_user": "true",
        }
        if "user_id" in request.GET:
            params_v1["user_id"] = request.GET.get("user_id")
        else:
            params_v1["screen_name"] = request.GET.get("screen_name")
        params_v2 = {
            "tweet.fields": "context_annotations,created_at,entities,geo,in_reply_to_user_id,lang,public_metrics,reply_settings",
            "max_results": 5,
        }
        options_v2 = {
            "params": params_v2,
        }
        options_v1 = {
            "params": params_v1,
        }

        async def fetch_data():
            pass

        response_v1 = Request.make(endpoint_v1, options_v1)
        response_v2 = Request.make(endpoint_v2, options_v2)
        return JsonResponse(response_v1)


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
        return JsonResponse(response, safe=False)


class UserShow(View):
    def get(self, request):
        endpoint = Api.show_user()
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
