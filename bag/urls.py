from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add_to_bag/<int:item_id>/', views.add_to_bag, name='add_to_bag'),
    path('update_bag_item/<int:item_id>/', views.update_bag_item, name='update_bag_item'),
]