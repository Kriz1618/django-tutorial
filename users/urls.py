from django.urls import path

from .views import LoginView, RefreshTokenView, RegisterView, LogoutView, ProtectedView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh", RefreshTokenView.as_view(), name="token_refresh"),
]
