from django.urls import path

from .views import LoginView, RefreshTokenView, RegisterView, Logout

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('token/refresh', RefreshTokenView.as_view(), name='token_refresh'),
]
