# 对应app的路由
from django.urls import path
from . import views

urlpatterns = [
    path('sql/', views.sql_data),
    path('template/', views.template),
    path('address/', views.address),
    path('info_data/', views.info_data),
    path('count/', views.detail_count),
]