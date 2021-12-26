from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', include('tweet.urls')),
    # path('api/', include('tweet_api.urls'))
    path("2/users/", include("users.urls")),
]
