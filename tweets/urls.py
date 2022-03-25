from django.urls import path

from tweets.views import tweet_lookup, manage_tweet, tweet_search_with_replies

app_name = "tweets"

urlpatterns = [
    path("", manage_tweet, name="manage_tweet"),
    path("<int:id>", tweet_lookup, name="tweet_lookup"),
    path("search/recent/<int:id>/<str:username>", tweet_search_with_replies, name="tweet_search_with_replies"),
]
