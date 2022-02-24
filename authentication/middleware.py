import jwt
import requests

from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.middleware import get_user

# from request.requests import Request
from authentication.utils import get_token_auth_header, jwt_decode_token
from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# from django.contrib.auth.models import User

from users.models import Account


class AuthorizationMiddleware:

    key = settings.TWITTER_API_KEY

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            user, token = JSONWebTokenAuthentication().authenticate(Request(request))
            user_id = user.username.split(".")[1]
            account = Account.objects.get(twitter_user_id=user_id)
            request.user = account
        except Account.DoesNotExist:
            if request.path == "/2/users/whoami/":
                request.user.twitter_user_id = user_id
                pass
        except (Exception, Account.DoesNotExist) as e:
            if request.path.startswith("/admin/"):
                pass
            else:
                return JsonResponse(
                    {"error": "You are not authorize", "code": 401}, status=401
                )
        response = self.get_response(request)
        return response


# curl --request GET \
#   --url http://127.0.0.1:8000/2/users/whoami/twitter|875905303245729793 \
#   --header 'content-type: application/json' \
#   --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0d2l0dGVyfDg3NTkwNTMwMzI0NTcyOTc5MyJ9.uGIyoNRXZWhzxciAk-X110ny0yRfAX7_6oX22S9XmMY' \

# payload = jwt.decode(token, key="Hello", algorithms="HS256")
# try:
#     auth_token = request.headers.get("Authorization", None)
#     sub = request.path.split("/")[-1]
#     token = auth_token.split(" ")[1]

#     url = f"{settings.AUTH0_DOMAIN}/api/v2/users/{sub}"
#     response = requests.get(url, headers={
#         "Authorization": f"Bearer {settings.AUTH0_API_TOKEN}"
#     })
#     print(response.json())

#     # TODO: keep api private
#     # TODO: Authenticate user from backend using django-social-login or Auth0-django-sdk


#     # response = await Request.make(
#     #     url,
#     #     {
#     #         "headers": {
#     #             "Authorization": f"Bearer {settings.AUTH0_API_TOKEN}",
#     #             "Content-Type": "application/json charset=utf-8",
#     #         }
#     #     },
#     # )
#     # print(response)
#     if token:
#         payload = jwt.decode(token, key=self.key, algorithms="HS256")
#         sub_id = payload["sub"].split("|")[1]
#         # if sub_id != id:
#         #     ...
# except:
#     return JsonResponse(
#         {"message": "Wait!! Who are you?"}, status=403, safe=False
#     )

# if not token or "/2/users/whoami/twitter" in request.path:
#     ...

# print(request.META["HTTP_AUTHORIZATION"])

# response = self.get_response(request)
# return response
