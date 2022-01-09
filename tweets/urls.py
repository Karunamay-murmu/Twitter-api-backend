from django.urls import path

from tweets.views import user_timeline

app_name = "tweets"

urlpatterns = [
    path("user_timeline.json", user_timeline, name="user_timeline"),
]
