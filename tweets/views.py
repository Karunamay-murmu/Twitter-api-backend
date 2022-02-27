import json

from django.http.response import JsonResponse

from request.api import Api
from request.requests import Request

params = {
    "tweet.fields": "id,text,attachments,author_id,context_annotations,created_at,entities,in_reply_to_user_id,conversation_id,lang,public_metrics,referenced_tweets,reply_settings,source",
    "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,attachments.media_keys,entities.mentions.username",
    "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
    "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
}


async def tweet_lookup(request, id):
    url = Api.tweet_lookup(id)
    params = {
        "tweet.fields": "id,text,attachments,author_id,context_annotations,created_at,entities,in_reply_to_user_id,conversation_id,lang,public_metrics,referenced_tweets,reply_settings,source",
        "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,attachments.media_keys",
        "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
        "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
    }
    options = {
        "params": params,
    }

    try:
        response = await Request.make(url, options)
        if response["status"] == 200:
            return JsonResponse(response["response"], safe=False, status=200)
    except:
        return JsonResponse(
            {"error": {"message": "Error occured while fetching data", "status": 500}},
            status=500,
        )


async def manage_tweet(request):
    data = json.loads(request.body)
    try:
        user = request.user
        url = Api.manage_tweet()
        body = {"text": data.get("text", "")}
        if data.get("reply"):
            body.update(
                {
                    "reply": {
                        "in_reply_to_tweet_id": data.get("reply", {}).get(
                            "in_reply_to_tweet_id", ""
                        ),
                        "exclude_reply_user_ids": data.get("reply", {}).get(
                            "exclude_reply_user_ids", ""
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
        print(response)
        return JsonResponse(response["response"], safe=False, status=response["status"])
    except Exception as e:
        return JsonResponse({"error": e, "status": 500}, status=500)


# async def tweets_lookup(request):
#     url = Api.tweets_lookup([1482375313598423043])
#     params = {
#         "tweet.fields": "id,text,author_id,created_at,in_reply_to_user_id,conversation_id,lang,referenced_tweets",
#         "expansions": "author_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id",
#         "user.fields": "name,username",
#     }
#     options = {
#         "params": params,
#     }
#     response = await Request.make(url, options)
#     if response["status"] == 200:
#         return JsonResponse(response["response"], safe=False, status=200)
#     return JsonResponse({
#         "error": {
#             "message": "Error occured while fetching data",
#             "status": 500
#         }
#     }, status=500)


async def user_timeline(request, id):
    url = Api.user_timeline(id)
    params = {
        "tweet.fields": "id,text,attachments,author_id,context_annotations,created_at,entities,in_reply_to_user_id,conversation_id,lang,public_metrics,referenced_tweets,reply_settings,source",
        "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,attachments.media_keys",
        "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
        "user.fields": "created_at,location,profile_image_url,public_metrics,url,verified,description,entities,pinned_tweet_id",
        "exclude": "replies",
    }
    options = {
        "params": params,
    }
    response_v2 = await Request.make(url, options)
    if response_v2["status"] == 200:
        return JsonResponse(response_v2["response"], safe=False, status=200)
    return JsonResponse(
        {"error": {"message": "Error occured while fetching data", "status": 500}},
        status=500,
    )


async def tweet_search_with_replies(request, id, username):
    url = Api.tweet_search()
    params["query"] = f"conversation_id:{id} is:reply"
    params["max_results"] = 30
    options = {
        "params": params,
    }
    response = await Request.make(url, options)
    if response["status"] == 200:
        return JsonResponse(response["response"], safe=False, status=200)
    return JsonResponse(
        {"error": {"message": "Error occured while fetching data", "status": 500}},
        status=500,
    )
