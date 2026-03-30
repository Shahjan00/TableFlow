from django.urls import path
from .views import *

urlpatterns = [
    path('shop/', shop_list_create),
    path('menu/', menu_list_create),
    path('tables/', table_list_create),
]