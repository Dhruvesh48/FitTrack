from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_page, name='product_page'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
]