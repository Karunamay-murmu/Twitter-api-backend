from django.urls import path


from users.views import (
    SearchUserByQuery,
    UserShow,
    manage_users_friendships,
    user_by_username,
    user_liked_tweets,
    user_followers,
    whoami,
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
    path("whoami/", whoami, name="whoami"),

    # v1.1 endpoints
    path("friendships/manage/<str:source_user_id>/<str:target_user_id>", manage_users_friendships, name="users_friendship"),
    path("search.json", SearchUserByQuery.as_view(), name="search_users"),
    path("show.json", UserShow.as_view(), name="users_show"),

]
