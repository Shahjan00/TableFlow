from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Menu
from .serializers import MenuSerializer
from rest_framework import status

@api_view(['GET', 'POST'])
def menu_list_create(request):
    
    if request.method == 'GET':
        menu = Menu.objects.all()
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)