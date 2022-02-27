from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("2/users/", include("users.urls")),
    path("2/tweets/", include("tweets.urls")),
    path("", include("django.contrib.auth.urls")),
    path("", include("social_django.urls")),
]
