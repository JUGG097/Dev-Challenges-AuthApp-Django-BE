from django.urls import path
from .views import AuthView, UserView, health_check

urlpatterns = [
    path("check", health_check, name="health_check"),
    path(
        "auth/signup", AuthView.as_view({"post": "register_user"}), name="user_signup"
    ),
    path("auth/login", AuthView.as_view({"post": "login_user"}), name="user_login"),
    path(
        "auth/refreshToken",
        AuthView.as_view({"post": "refresh_token"}),
        name="refresh_token",
    ),
    path("user/profile", UserView.as_view({"get": "get"}), name="user_profile"),
    path(
        "user/editProfile", UserView.as_view({"put": "put"}), name="edit_user_profile"
    ),
]
