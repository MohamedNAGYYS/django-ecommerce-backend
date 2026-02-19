from django.contrib import admin
from .models import Product, Order, OrderItem, Payment, Cart, CartItem, Category



admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
