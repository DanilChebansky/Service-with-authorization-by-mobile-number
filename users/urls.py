from django.urls import path

from users.apps import UsersConfig
from users.views import (
    UserRegisterAPIView,
    UserConfirmAPIView,
    UserUpdateAPIView,
    UserProfileAPIView,
    UserListAPIView,
    UserDestroyAPIView,
)

from django.contrib.auth.views import LogoutView
app_name = UsersConfig.name

urlpatterns = [
    path("login/confirm/", UserConfirmAPIView.as_view(), name="confirm"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", UserListAPIView.as_view(), name="user_list"),
    path("login/", UserRegisterAPIView.as_view(), name="login"),
    path("<int:pk>/", UserProfileAPIView.as_view(), name="user_detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_delete"),
]
