from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

def index(request):
    return JsonResponse({
        "project": "TableFlow",
        "status": "ok",
        "message": "TableFlow API is running",
        "routes": {
            "auth": "/auth/",
            "shops": "/shops/",
            "orders": "/orders/"
        }
    })