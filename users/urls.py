from django.urls import path

from users.views import (
    GetUserTweetById, 
    SearchUserByQuery,
    UserShow,
    user_by_username,
    user_liked_tweets,
    user_followers,
)
from tweets.views import user_timeline

app_name = "users"

urlpatterns = [
    path(
        "by/username/<str:username>",
        user_by_username,
        name="get_user_by_username",
    ),
    path("<int:id>/tweets", user_timeline, name="user_timeline"),
    path("<int:id>/liked_tweets", user_liked_tweets, name="user_liked_tweets"),
    path("<int:id>/<str:path>", user_followers, name="user_followers"),
    # path("<int:id>/following", user_following, name="user_followers"),

    # v1.1 endpoints
    path("search.json", SearchUserByQuery.as_view(), name="search_users"),
    path("show.json", UserShow.as_view(), name="users_show"),
]
