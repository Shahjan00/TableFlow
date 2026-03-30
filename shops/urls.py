from django.urls import path
from .views import *

urlpatterns = [
    path('menu/', menu_list_create),
]