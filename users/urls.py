from django.urls import path

from users.apps import UsersConfig
from users.views import (
    UserRegisterAPIView,
    UserUpdateAPIView,
    UserProfileAPIView,
    UserListAPIView,
    UserDestroyAPIView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = UsersConfig.name


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", UserListAPIView.as_view(), name="user_list"),
    path("login/", UserRegisterAPIView.as_view(), name="login"),
    path("<int:pk>/", UserProfileAPIView.as_view(), name="user_detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_delete"),
]
