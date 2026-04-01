from django.urls import path, include
from .views import *

urlpatterns = [
    path('',order_list_create),
    path('<int:id>', order_detail),
    path('menu/<str:qr_token>/', table_menu_by_qr),
    path('order/<str:qr_token>/', create_order_by_qr),
    
]