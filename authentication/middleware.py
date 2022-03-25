from django.http import JsonResponse
from django.conf import settings

from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import Account


class AuthorizationMiddleware:

    key = settings.TWITTER_API_KEY

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            user, _ = JSONWebTokenAuthentication().authenticate(Request(request))
            user_id = user.username.split(".")[1]
            account = Account.objects.get(twitter_user_id=user_id)
            request.user = account
        except Account.DoesNotExist:
            if request.path == "/2/users/whoami/":
                request.user.twitter_user_id = user_id
                pass
        except Exception:
            if not request.path.startswith("/admin/"):
                return JsonResponse(
                    {"error": "You are not authorize", "code": 401}, status=401
                )
        response = self.get_response(request)
        return response
