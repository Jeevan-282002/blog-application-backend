from django.urls import path
from .views import RegisterUserProfileView, UserLoginView

urlpatterns = [
    path('register/', RegisterUserProfileView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]