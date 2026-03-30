from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status

@api_view(['GET', 'POST'])
def menu_list_create(request): 
    
    if request.method == 'GET':
        shop_id = request.query_params.get('shop')

        if shop_id:
            menu = Menu.objects.filter(shop_id=shop_id)
        else:
            menu = Menu.objects.all()
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
def shop_list_create(request):
    if request.method == 'GET':
        shops =  Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ShopSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
def table_list_create(request):
    if request.method == 'GET':
        shop_id = request.query_params.get('shop')

        if shop_id:
            tables = Table.objects.filter(shop_id=shop_id)
        else:
            tables = Table.objects.all()
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
