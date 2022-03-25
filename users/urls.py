from django.urls import path


from users.views import (
    home_timeline,
    user_timeline,
    user_show,
    manage_users_friendships,
    user_by_username,
    user_liked_tweets,
    user_followers,
    whoami,
)

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
    path("home_timeline", home_timeline, name="home_timeline"),

    path("friendships/manage/<str:source_user_id>/<str:target_user_id>", manage_users_friendships, name="users_friendship"),
    path("show.json", user_show, name="users_show"),

]
