import json
from os import access
from urllib import response

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.middleware.csrf import get_token
from asgiref.sync import sync_to_async

from request.api import Api
from request.requests import Request
from users.models import Account
from tweets.views import tweet_lookup

# Create your views here.

BASE_URL = settings.TWITTER_API_BASE_URL
BASE_URL_V1 = settings.TWITTER_API_BASE_URL_V1


async def user_by_username(request, username):
    endpoint_v1 = Api.show_user()
    endpoint_v2 = Api.user_by_username(username)

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
            pinned_tweet_id = response_v2["response"]["data"]["pinned_tweet_id"]
            res = await tweet_lookup(None, pinned_tweet_id)
            tweet = json.loads(res.content.decode())
            response_v2["response"]["pinned_tweet"] = tweet
        response_v2["response"]["data"]["profile_banner_url"] = response_v1[
            "response"
        ].get("profile_banner_url", None)
        return JsonResponse(response_v2["response"], safe=False, status=200)
    return JsonResponse(
        {"error": {"message": "Error occured while fetching data", "status": 500}},
        status=500,
    )


async def user_liked_tweets(request, id):
    url = Api.user_liked_tweets(id)
    options = {
        "params": {
            "tweet.fields": "id,text,attachments,author_id,context_annotations,created_at,entities,in_reply_to_user_id,conversation_id,lang,public_metrics,referenced_tweets,reply_settings,source",
            "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,attachments.media_keys,entities.mentions.username",
            "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
            "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
            "max_results": 30,
        }
    }
    response = await Request.make(url, options)
    if response["status"] == 200:
        return JsonResponse(response["response"], safe=False, status=200)
    return JsonResponse(
        {"error": {"message": "Error occured while fetching data", "status": 500}},
        status=500,
    )


async def user_followers(request, id, path):
    url = Api.user_followers(path, id)
    options = {
        "params": {
            "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
        },
    }
    response = await Request.make(url, options)
    if response["status"] == 200:
        return JsonResponse(response["response"], safe=False, status=200)
    return JsonResponse(
        {"error": {"message": "Error occured while fetching data", "status": 500}},
        status=500,
    )


async def whoami(request):
    if request.method == "GET":
        id = request.user.twitter_user_id
        url = f"{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/api/v2/users/twitter|{id}"
        print(url)
        try:
            user = await sync_to_async(Account.objects.get, thread_sensitive=True)(
                twitter_user_id=id
            )
        except Account.DoesNotExist:
            response = await Request.make(
                url,
                {
                    "headers": {
                        "Authorization": f"Bearer {settings.SOCIAL_AUTH_AUTH0_API_TOKEN}",
                    }
                },
            )
            if response["status"] == 200:
                res = response["response"]
                nickname = res.get("nickname", None)
                name = res.get("name", None)
                picture = res.get("picture", None)
                ip = res.get("last_ip", None)
                screen_name = res.get("screen_name", None)
                twitter_user_id = res["identities"][0]["user_id"]
                access_token = res["identities"][0]["access_token"]
                access_token_secret = res["identities"][0]["access_token_secret"]
                user = await sync_to_async(
                    Account.objects.create, thread_sensitive=True
                )(
                    nickname=nickname,
                    name=name,
                    picture=picture,
                    twitter_user_id=twitter_user_id,
                    access_token=access_token,
                    access_token_secret=access_token_secret,
                    last_ip=ip,
                    screen_name=screen_name,
                )
            else:
                return JsonResponse(
                    {"response": response["response"]},
                    safe=False,
                    status=response["status"],
                )
        return JsonResponse(
            {
                "user": user.to_dict(),
                "csrf_token": get_token(request),
            },
            safe=True,
            status=200,
        )
    return JsonResponse({"message": "Bad request"}, status=400, safe=False)


async def manage_users_friendships(request, source_user_id, target_user_id):
    try:
        user = request.user
        friendship = request.GET.get("friendship", "show")
        if friendship == "show":
            url = Api.show_friendship(source_user_id, target_user_id)
            response = await Request.make(url)
        if friendship == "create":
            url = Api.create_friendship(source_user_id)
            body = json.dumps({"target_user_id": target_user_id})
            response = await Request.make(
                url,
                {"method": "POST", "body": body},
                access_token=user.access_token,
                access_token_secret=user.access_token_secret,
            )
        if friendship == "destroy":
            url = Api.destroy_friendship(source_user_id, target_user_id)
            response = await Request.make(
                url,
                {"method": "DELETE"},
                access_token=user.access_token,
                access_token_secret=user.access_token_secret,
            )
        return JsonResponse(
            response["response"],
            safe=False,
            status=response["status"],
        )
    except Exception as e:
        return JsonResponse({"error": e, "status": 500}, status=500)


async def create_friendship(request, source_user_id, target_user_id):
    try:
        url = Api.create_friendship(source_user_id)
        body = json.dumps({"target_user_id": target_user_id})
        response = await Request.make(
            url,
            {"method": "POST", "body": body},
            access_token=request.user.access_token,
            access_token_secret=request.user.access_token_secret,
        )
        return JsonResponse(response["response"], safe=False, status=response["status"])
    except Exception as e:
        return JsonResponse({"error": e, "status": 500}, status=500)


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


def get_user_object(id):
    try:
        user = Account.objects.get(twitter_user_id=id)
        return user
    except Account.DoesNotExist:
        raise Exception("User not found")
