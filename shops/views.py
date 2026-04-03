from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from accounts.models import User
from shops.models import Staff

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def menu_list_create(request): 
    if request.user.role not in ['owner']:
        return Response({'error': 'Not allowed'}, status=403)
    if request.method == 'GET':
        shop_id = request.query_params.get('shop')
        menu = Menu.objects.filter(shop__user=request.user)

        if shop_id:
            menu = menu.filter(shop_id=shop_id)
        serializer = MenuSerializer(menu, many=True)
        if serializer.data:
            return Response(serializer.data)
        return Response({"message": "Not Have Any shop"})

    elif request.method == 'POST':
        shop_id = request.data.get('shop')
        if not Shop.objects.filter(id=shop_id, user=request.user).exists():
            return Response({'error': 'You can only manage menu for your own shop'}, status=403)

        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def shop_list_create(request):
    if request.user.role not in ['owner']:
        return Response({'error': 'Not allowed'}, status=403)
    if request.method == 'GET':
        shops =  Shop.objects.filter(user=request.user)
        # print(shops)
        serializer = ShopSerializer(shops, many=True)
        if serializer.data:
            return Response(serializer.data)
        return Response({"message": "Not Have Any shop"})
    elif request.method == 'POST':
        serializer = ShopSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def table_list_create(request):
    if request.user.role not in ['owner']:
        return Response({'error': 'Not allowed'}, status=403)
    if request.method == 'GET':
        shop_id = request.query_params.get('shop')
        tables = Table.objects.filter(shop__user=request.user)

        if shop_id:
            tables = tables.filter(shop_id=shop_id)
        serializer = TableSerializer(tables, many=True)
        if serializer.data:
            return Response(serializer.data)
        return Response({"message": "Not Have Any Table"})
    elif request.method == 'POST':
        shop_id = request.data.get('shop')
        if not Shop.objects.filter(id=shop_id, user=request.user).exists():
            return Response({'error': 'You can only manage tables for your own shop'}, status=403)

        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_staff(request, shop_id):
    if request.method == 'POST':
        shop = get_object_or_404(Shop, id=shop_id)

        if shop.user != request.user:
            return Response({"error":"not allowed"}, status=403)
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, email=user_id)

        if user.role != 'staff':
            return Response({"error": "Selected user is not staff"}, status=400)

        Staff.objects.get_or_create(user=user, shop=shop)
        shop.staff_members.add(user)
        return Response({"message": "Staff linked successfully"}, status=200)
