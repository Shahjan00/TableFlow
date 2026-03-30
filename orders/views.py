from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from shops.serializers import MenuSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def order_list_create(request):
    if request.method == 'GET':
        shop_id = request.query_params.get('shop')
        if shop_id:
            orders = Order.objects.filter(shop_id=shop_id)
        else:
            orders = Order.objects.all()

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PATCH'])
def order_detail(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found!'}, status=404)
        
    if request.method == 'GET':

        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        new_status = request.data.get('status')

        ALLOWED_STATUS = ['pending', 'ready', 'completed']

        if new_status not in ALLOWED_STATUS:
            return Response({'error': 'Invalid Status'}, status=400)
        
        order.status = new_status
        order.save()

        return Response({'message': 'Status Update Sussessfully'}, status=200)
    


