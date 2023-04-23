# 对应app的路由
from django.urls import path
from . import views

urlpatterns = [
    path('sql/', views.sql_data),
    path('template/', views.template),
    path('address/', views.address),
    path('count/', views.detail_count),
    path('get_data/', views.get_data),
    path('word_cloud/', views.word_cloud),
    path('search/', views.search),
]