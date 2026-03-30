from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

# Create your views here.

@api_view(['GET', 'POST'])
def order_list_create(request):
    if request.method == 'GET':
        orders = Order.objects.all()

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("inside error", status=status.HTTP_400_BAD_REQUEST)