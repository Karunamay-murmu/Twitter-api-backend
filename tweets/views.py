from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse

from request.api import Api
from request.requests import Request

async def user_timeline(request):
    endpoint_v1 = Api.users_timeline()
    endpoint_v2 = Api.get_user_tweets(request.GET.get("user_id"))

    params_v1 = {
        "tweet_mode": "extended",
        # "exclude_replies": "true",
        "trim_user": "true",
    }
    if "user_id" in request.GET:
        params_v1["user_id"] = request.GET.get("user_id")
    else:
        params_v1["screen_name"] = request.GET.get("screen_name")

    params_v2 = {
        "tweet.fields": "id,text,attachments,author_id,context_annotations,created_at,entities,in_reply_to_user_id,lang,public_metrics,referenced_tweets,reply_settings,source",
        "expansions": "author_id,in_reply_to_user_id,referenced_tweets.id.author_id,attachments.media_keys",
        "max_results": 20,
        "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
    }

    options_v1 = {
        "params": params_v1,
    }
    options_v2 = {
        "params": params_v2,
    }
    # response_v1 = await Request.make(endpoint_v1, options_v1)
    response_v2 = await Request.make(endpoint_v2, options_v2)

    # print(len(response_v2["data"]))
    # print(len(response_v1))
    # for idx, tweet in enumerate(response_v2["data"]):
    #     print(tweet["id"])
    #     print(response_v1[idx]["id_str"])
    #     if tweet["id"] == response_v1[idx]["id_str"]:
    #         response_v2["data"][idx]["extend_entites"] = response_v1[idx].get("extended_entities", None)
    # print(len(respo))
    # response = response_v1.update(response_v2)
    # print(response)
    return JsonResponse(response_v2, safe=False)

