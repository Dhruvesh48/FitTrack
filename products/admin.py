from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'category', 'rating', 'has_sizes', 'created_at']
    search_fields = ['name', 'sku']
    list_filter = ['category', 'created_at', 'has_sizes']
    
admin.site.register(Product, ProductAdmin)