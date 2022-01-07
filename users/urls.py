from django.urls import path

from users.views import (
    GetUserByUsername, 
    GetUserTweetById, 
    SearchUserByQuery,
    UserShow
)

app_name = "users"

urlpatterns = [
    path(
        "by/username/<str:username>",
        GetUserByUsername.as_view(),
        name="get_user_by_username",
    ),
    path("<int:id>/tweets", GetUserTweetById.as_view(), name="get_user_tweets"),
    
    # v1.1 endpoints
    path("search.json", SearchUserByQuery.as_view(), name="search_users"),
    path("show.json", UserShow.as_view(), name="users_show"),
]
