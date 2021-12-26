from django.urls import path

from users.views import GetUserByUsername

app_name = "users"

urlpatterns = [
    path("by/username/<str:username>", GetUserByUsername.as_view(), name="get_user_by_username"),
]
