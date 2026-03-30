from rest_framework import serializers
import uuid
from django.utils.text import slugify
import qrcode
from io import BytesIO
from django.core.files import File
from .models import *

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shop
        fields = ['id', 'name', 'logo', 'phone', 'address', 'is_active']

    def create(self, validated_data):
        request = self.context.get('request')
        # user = request.user
        user = User.objects.first()     # Change itttttttt 
        name = validated_data.get('name')
        base_slug = slugify(name)

        slug = base_slug
        counter = 1

        while Shop.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter +=1


        shop = Shop.objects.create(user=user,slug=slug, **validated_data)

        return shop

class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ['shop', 'table_name', 'qr_token', 'qr_code', 'is_active']
        read_only_fields = ['qr_token', 'qr_code']

    def create(self, validated_data):
        # generate unique token
        qr_token = str(uuid.uuid4())
        qr_url = f"http://127.0.0.1:8000/order/{qr_token}/"

        qr = qrcode.make(qr_url)

        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        file_name = f"table_{qr_token}.png"


        table = Table.objects.create(
            qr_token=qr_token,
            **validated_data
        )

        table.qr_code.save(file_name, File(buffer), save=True)

        return table