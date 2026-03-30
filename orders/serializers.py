from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'shop', 'table', 'status', 'items']
        read_only_fields = ['status']

    def validate(self, data):
        shop = data.get('shop')
        table = data.get('table')
        items = data.get('items')

        # Check table belongs to shop
        if table.shop != shop:
            raise serializers.ValidationError("Table does not belong to this shop")

        # Check menu items
        for item in items:
            menu_item = item['menu_item']

            if menu_item.shop != shop:
                raise serializers.ValidationError("Menu item not from this shop")

            if not menu_item.is_available:
                raise serializers.ValidationError(f"{menu_item.name} is not available")

        return data
        
    

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order
