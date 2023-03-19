# 对应app的路由
from django.urls import path
from . import views

urlpatterns = [
    path('sql/', views.sql_data),
    path('template/', views.template),
    path('address/', views.address),
    path('detail/', views.detail),
    path('count/', views.detail_count),
]