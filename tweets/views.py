from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse

from request.api import Api
from request.requests import Request

class UserTimeline(View):
     def get(self, request):
        endpoint = Api.users_timeline()
        print("endpoint: ", endpoint)
        params = {}
        if "user_id" in request.GET:
            params["user_id"] = request.GET.get("user_id")
        else:
            params["screen_name"] = request.GET.get("screen_name")
        options = {
            "params": params,
        }
        print(params)
        response = Request.make(endpoint, options)
        return JsonResponse(response, safe=False)

