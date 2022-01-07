from django.urls import path

from tweets.views import UserTimeline

app_name = "tweets"

urlpatterns = [
    path("user_timeline.json", UserTimeline.as_view(), name="user_timeline"),
]
