from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()), 
    path('token/refresh', TokenRefreshView.as_view()),
    path('register/', register),
]
