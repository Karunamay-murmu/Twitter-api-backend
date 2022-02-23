from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("2/users/", include("users.urls")),
    path("2/tweets/", include("tweets.urls")),
    path("2/oauth2/", include("authentication.urls")),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # auth0login\urls.py
    path("", include("django.contrib.auth.urls")),
    path("", include("social_django.urls")),
    # urlpatterns = [
    #     path('', views.index),
    #     path('dashboard', views.dashboard),
    #     path('logout', views.logout),
    # ]
]
