from django.db import models
from accounts.models import User

# Create your models here.

class Shop(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='shop')

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    logo = models.ImageField(upload_to='images/',blank=True, null=True)

    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE, related_name='tables')
    table_name = models.CharField(max_length=50)

    qr_token = models.CharField(max_length=100, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shop.name} - {self.table_name}"
    

class Menu(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='menu')

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"
    

