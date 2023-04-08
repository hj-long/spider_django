# 对应app的路由
from django.urls import path
from . import views

urlpatterns = [
    path('sql/', views.sql_data),
    path('template/', views.template),
    path('address/', views.address),
    path('g_power/', views.g_power),
    path('count/', views.detail_count),
    path('g_inputRev/', views.g_inputRev),
    path('g_outputRev/', views.g_outputRev),
    path('g_torque/', views.g_torque),
    path('g_ratio/', views.g_ratio),
    path('get_data/', views.get_data),
]