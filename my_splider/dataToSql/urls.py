# 对应app的路由
from django.urls import path
from . import views
from . import dataView

urlpatterns = [
    path('sql/', views.sql_data),
    path('template/', views.template),
    path('address/', views.address),
    path('count/', views.detail_count),
    path('get_data/', views.get_data),
    path('word_cloud/', views.word_cloud),
    path('search/', views.search),
    path('recommend/', views.recommend),
    # 额定功率与许用扭矩分析
    path('data_view1/', dataView.data_view1),
    # 价格和销量分析
    path('data_view2/', dataView.data_view2),
]