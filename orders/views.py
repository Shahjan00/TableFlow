from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from shops.serializers import MenuSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    if request.user.role not in ['owner', 'staff']:
        return Response({'error': 'Not allowed'}, status=403)
    if request.method == 'GET':
        shop_id = request.query_params.get('shop')
        orders = Order.objects.filter(shop__user=request.user)
        if shop_id:
            orders = orders.filter(shop_id=shop_id)

        serializer = OrderSerializer(orders, many=True)
        if serializer.data:
            return Response(serializer.data)
        return Response({"message": "Not Have Any Order"})
    elif request.method == 'POST':
        shop_id = request.data.get('shop')
        if not Shop.objects.filter(id=shop_id, user=request.user).exists():
            return Response({'error': 'You can only create orders for your own shop'}, status=403)

        serializer = OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def order_detail(request,id):
    if request.user.role == 'owner':
        order = Order.objects.filter(id=id, shop__user=request.user).first()
    elif request.user.role == 'staff':
        order = Order.objects.filter(id=id, shop__staff_members=request.user).first()
    else:
        return Response({'error': 'Not allowed'}, status=403)

    if not order:
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
    elif request.method == 'DELETE':
        order.delete()
        return Response({'message': 'Order Deleted'}, status=200)
    

@api_view(['GET'])
def table_menu_by_qr(request, qr_token):
    table = get_object_or_404(Table,qr_token=qr_token,is_active=True, shop__is_active=True)
    
    menu = Menu.objects.filter(shop=table.shop)
    serializer = MenuSerializer(menu, many=True)

    return Response(
        {
            "shop": {"id": table.shop.id, "name" : table.shop.name},
            "table": {"id" : table.id, "table_name" : table.table_name},
            "menu" : serializer.data
        },
        status=status.HTTP_200_OK
    )
    
@api_view(['POST'])
def create_order_by_qr(request,qr_token):
    table = get_object_or_404(Table,qr_token=qr_token,is_active=True, shop__is_active=True)
    shop = table.shop
    
    data = request.data.copy()

    data['shop'] = shop.id
    data['table'] = table.id

    serializer = OrderSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
