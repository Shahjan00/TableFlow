from django.urls import path
from .views import *

urlpatterns = [
    path('',order_list_create),
    path('<int:id>', order_detail),

]