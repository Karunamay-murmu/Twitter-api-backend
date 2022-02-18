from django.urls import path

from authentication.views import user_auth_login, oauth_request_token
app_name = "authentication"

urlpatterns = [
    path("login/<str:token>/<str:verifier>", user_auth_login, name="login"),
    path("request_token", oauth_request_token, name="oauth_request_token"),
    # path("callback", oauth_callback, name="callback"),
]