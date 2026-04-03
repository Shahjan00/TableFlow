from django.contrib import admin
from .models import Shop , Table, Menu, Staff

# Register your models here.

admin.site.register(Shop)
admin.site.register(Table)
admin.site.register(Menu)
admin.site.register(Staff)