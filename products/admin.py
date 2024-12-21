from django.contrib import admin
from .models import Product, Wishlist

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'category', 'rating', 'has_sizes', 'created_at']
    search_fields = ['name', 'sku']
    list_filter = ['category', 'created_at', 'has_sizes']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')

    
admin.site.register(Product, ProductAdmin)
admin.site.register(Wishlist, WishlistAdmin)