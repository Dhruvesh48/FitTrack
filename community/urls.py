from django.urls import path
from . import views


urlpatterns = [
    path('', views.community_list, name='community_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]