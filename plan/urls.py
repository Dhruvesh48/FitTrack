from django.urls import path
from . import views

urlpatterns = [
    path('', views.exercise_plan_list, name='exercise_plan_list'),
    path('plan_list/', views.plan_list, name='plan_list'),
]