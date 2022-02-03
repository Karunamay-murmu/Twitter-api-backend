from django.urls import path

from tweets.views import user_timeline, tweet_lookup, tweets_lookup, tweet_search_with_replies

app_name = "tweets"

urlpatterns = [
    path("username/<str:username>", user_timeline, name="user_timeline"),
    path("<int:id>", tweet_lookup, name="tweet_lookup"),
    path("", tweets_lookup, name="tweets_lookup"),
    path("search/recent/<int:id>/<str:username>", tweet_search_with_replies, name="tweet_search"),
]
