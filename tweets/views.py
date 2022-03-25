import json

from django.http.response import JsonResponse

from request.api import Api
from request.requests import Request


async def friendship_lookup(user, ids):
    try:
        url = Api.friendship_lookup() + f"?user_id={ids}"
        return await Request.make(
            url,
            access_token=user.access_token,
            access_token_secret=user.access_token_secret,
        )
    except Exception as e:
        return JsonResponse({"error": e}, status=500, safe=False)


async def friendship_show(source, target):
    try:
        url = Api.friendship_show()
        options = {
            "params": {
                "source_id": source,
                "target_id": target,
            }
        }
        response = await Request.make(url, options)
        return JsonResponse(response["response"], safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500, safe=False)


async def tweet_lookup(request, id):
    try:
        url = Api.tweet_lookup(id)
        response = await Request.make(
            url,
            {
                "params": {
                    "tweet.fields": "id,text,attachments,author_id,context_annotations,created_at,entities,in_reply_to_user_id,conversation_id,lang,public_metrics,referenced_tweets,reply_settings,source",
                    "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,attachments.media_keys,entities.mentions.username",
                    "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
                    "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
                },
            },
        )
        try:
            users = response["response"]["includes"]["users"]
            ids = ",".join([user["id"] for user in users])
            friendships = await friendship_lookup(user=request.user, ids=ids)
            for tweet_user in users:
                for user in friendships["response"]:
                    if tweet_user["id"] == user["id_str"]:
                        tweet_user["connections"] = user["connections"]
                        break
        except:
            pass
        return JsonResponse(response["response"], safe=False, status=200)
    except Exception as e:
        return JsonResponse(
            {"error": e or "action not allowed", "status": 500}, status=500
        )


async def manage_tweet(request):
    data = json.loads(request.body)
    try:
        user = request.user
        action = request.GET.get("tweet", None)
        response = None
        if action == "destroy":
            id = data.get("id", None)
            url = Api.manage_tweet() + "/" + id
            response = await Request.make(
                url,
                {"method": "DELETE"},
                access_token=user.access_token,
                access_token_secret=user.access_token_secret,
            )
            return JsonResponse(
                response["response"], safe=False, status=response["status"]
            )
        if action == "create":
            url = Api.manage_tweet()
            body = {"text": data.get("text", "")}
            if data.get("reply"):
                body.update(
                    {
                        "reply": {
                            "in_reply_to_tweet_id": data["reply"].get(
                                "in_reply_to_tweet_id", ""
                            ),
                            "exclude_reply_user_ids": data["reply"].get(
                                "exclude_reply_user_ids", []
                            ),
                        }
                    }
                )
            if data.get("media"):
                body.update(
                    {
                        "media": {
                            "media_ids": data.get("media", {}).get("media_ids", ""),
                            "tagged_user_ids": data.get("media", {}).get(
                                "tagged_user_ids", ""
                            ),
                        }
                    }
                )
            response = await Request.make(
                url,
                {
                    "method": "POST",
                    "body": json.dumps(body),
                },
                access_token=user.access_token,
                access_token_secret=user.access_token_secret,
            )
            tweet_res = await tweet_lookup(request, response["response"]["data"]["id"])
            tweet = json.loads(tweet_res.content.decode())
            return JsonResponse({"data": tweet}, safe=False, status=response["status"])
    except Exception as e:
        return JsonResponse(
            {"error": e or "action not allowed", "status": 500}, status=500
        )


async def tweet_search_with_replies(request, id, username):
    try:
        url = Api.tweet_search()
        options = {
            "params": {
                "query": f" conversation_id:{id} OR url:{id} is:reply -is:retweet to:{username}",
                "tweet.fields": "id,text,attachments,author_id,context_annotations,created_at,entities,in_reply_to_user_id,conversation_id,lang,public_metrics,referenced_tweets,reply_settings,source",
                "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,attachments.media_keys,entities.mentions.username",
                "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
                "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
            },
        }
        response = await Request.make(url, options)
        return JsonResponse(response["response"], safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, safe=False, status=500)
