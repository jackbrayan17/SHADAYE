from django.contrib import admin
from .models import Product, Order, OrderItem, Testimonial

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name', 'category')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'created_at')
    list_filter = ('status',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("customer", "comment", "rating", "approved", "created_at")  # Ensure all exist
    list_filter = ("approved",)  # Ensure 'approved' exists in models.py
    search_fields = ("customer", "comment")
   
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
