from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_page, name='product_page'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]