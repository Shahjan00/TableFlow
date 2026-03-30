from django.db import models

# Create your models here.

from shops.models import *

class Order(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
    table = models.ForeignKey(Table, on_delete=models.CASCADE,related_name='orders')

    # menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    # quantity = models.IntegerField()

    STATUS = (
        ('pending', "PENDING"),
        ('ready',  'READY'),
        ('completed', 'COMPLETED')
    )

    status = models.CharField(choices=STATUS, max_length=15, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

