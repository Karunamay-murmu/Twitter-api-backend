from django.urls import path

from authentication.views import user_auth_login, oauth_callback

app_name = "authentication"

urlpatterns = [
    path("login", user_auth_login, name="login"),
    path("callback", oauth_callback, name="callback"),
]