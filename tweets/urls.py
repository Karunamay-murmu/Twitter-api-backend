from django.urls import path

from tweets.views import user_timeline, tweet_lookup, tweets_lookup

app_name = "tweets"

urlpatterns = [
    path("username/<str:username>", user_timeline, name="user_timeline"),
    path("<int:id>", tweet_lookup, name="tweet_lookup"),
    path("", tweets_lookup, name="tweets_lookup"),
]
