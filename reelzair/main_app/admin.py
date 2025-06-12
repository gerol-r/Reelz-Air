from django.contrib import admin
from .models import Cart, Order, CartItem, Product

# Register your models here.

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Product)