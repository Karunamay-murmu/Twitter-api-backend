import json

from django.http import JsonResponse
from django.conf import settings
from django.middleware.csrf import get_token
from asgiref.sync import sync_to_async

from request.api import Api
from request.requests import Request
from users.models import Account
from tweets.views import tweet_lookup, friendship_lookup


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
            res = await tweet_lookup(request, pinned_tweet_id)
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


async def user_timeline(request, id):
    try:
        url = Api.user_timeline(id)
        options = {
            "params": {
                "tweet.fields": "id,text,attachments,author_id,context_annotations,created_at,entities,in_reply_to_user_id,conversation_id,lang,public_metrics,referenced_tweets,reply_settings,source",
                "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,attachments.media_keys,entities.mentions.username",
                "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
                "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
                "exclude": "replies",
            }
        }
        response = await Request.make(url, options)
        if response["response"]["meta"]["result_count"] > 0:
            users = response["response"]["includes"]["users"]
            ids = ",".join([user["id"] for user in users])
            friendship = await friendship_lookup(user=request.user, ids=ids)
            for tweet_user in users:
                for user in friendship["response"]:
                    if tweet_user["id"] == user["id_str"]:
                        tweet_user["connections"] = user["connections"]
                        break
        return JsonResponse(response["response"], safe=False, status=response["status"])
    except Exception as e:
        return JsonResponse({"error": e, "status": 500}, status=500)


async def user_liked_tweets(request, id):
    try:
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
        users = response["response"]["includes"]["users"]
        ids = ",".join([user["id"] for user in users])
        friendship = await friendship_lookup(user=request.user, ids=ids)
        for tweet_user in users:
            for user in friendship["response"]:
                if tweet_user["id"] == user["id_str"]:
                    tweet_user["connections"] = user["connections"]
                    break
        return JsonResponse(response["response"], safe=False, status=200)
    except Exception as e:
        return JsonResponse(
            {"error": {"message": e, "status": 500}},
            status=500,
        )


async def user_followers(request, id, path):
    try:
        url = Api.user_followers(path, id)
        options = {
            "params": {
                "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
            },
        }
        response = await Request.make(url, options)
        data = response["response"]["data"]
        ids = ",".join([user["id"] for user in data])
        friendship = await friendship_lookup(user=request.user, ids=ids)
        for idx, user in enumerate(friendship["response"]):
            data[int(idx)]["connections"] = user["connections"]
        return JsonResponse(response["response"], safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500, safe=False)


async def whoami(request):
    if request.method == "GET":
        id = request.user.twitter_user_id
        url = f"{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/api/v2/users/twitter|{id}"
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
            url = Api.friendship_show()
            options = {
                "params": {
                    "source_id": source_user_id,
                    "target_id": target_user_id,
                }
            }
            response = await Request.make(url, options)
        if friendship == "create" or friendship == "mute" or friendship == "block":

            if friendship == "create":
                url = Api.create_friendship(source_user_id)
            elif friendship == "mute":
                url = Api.mute_friendship(source_user_id)
            elif friendship == "block":
                url = Api.block_friendship(source_user_id)

            body = json.dumps({"target_user_id": target_user_id})
            response = await Request.make(
                url,
                {"method": "POST", "body": body},
                access_token=user.access_token,
                access_token_secret=user.access_token_secret,
            )

        if friendship == "destroy" or friendship == "unmute" or friendship == "unblock":
            if friendship == "destroy":
                url = Api.destroy_friendship(source_user_id, target_user_id)
            elif friendship == "unmute":
                url = Api.unmute_friendship(source_user_id, target_user_id)
            elif friendship == "unblock":
                url = Api.unblock_friendship(source_user_id, target_user_id)

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


async def home_timeline(request):
    user = request.user
    url = Api.users_home_timeline()
    try:
        response = await Request.make(
            url=f"{url}?count=50&trim_user=false&exclude_replies=true&tweet_mode=extended",
            access_token=user.access_token,
            access_token_secret=user.access_token_secret,
        )
        ids = ",".join([tweet["user"]["id_str"] for tweet in response["response"]])
        friendship = await friendship_lookup(user=user, ids=ids)
        for tweet in response["response"]:
            for user in friendship["response"]:
                if tweet["user"]["id_str"] == user["id_str"]:
                    tweet["user"]["connections"] = user["connections"]
                    break
        return JsonResponse(response["response"], safe=False, status=response["status"])
    except Exception as e:
        return JsonResponse({"error": e, "status": 500}, status=500)


def user_show(self, request):
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
