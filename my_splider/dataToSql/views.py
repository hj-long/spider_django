from django.shortcuts import render
# from django.http import HttpResponse
from dataToSql.models import GoodsInfo, GoodsDetail
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
# 从数据库中读取数据, 返回json格式数据
@api_view(['GET'])
def sql_data(request):
    # 从数据库中读取数据id前10条
    goods_info = GoodsInfo.objects.filter(id__lte=10)
    goods = []
    for i in goods_info:
        item = {
            'id': i.id,
            'title': i.title,
            'price': i.price,
            'sale_sum': i.sale_sum,
            'link': i.link,
            'detail': i.detail,
            'address': i.address,
            'factory_name': i.factory_name,
        }
        goods.append(item)
    
    # 将数据转换为json格式
    return Response(goods)

# 读取地址信息
@api_view(['GET'])
def address(request):
    # 从数据库中读取数据id前10条
    goods_info = GoodsInfo.objects.filter(id__lte=10)
    address = []
    for i in goods_info:
        address_info = i.address.split(' ')
        item = {
            'id': i.id,
            'address': i.address,
            'city': address_info[1],
        }       
        address.append(item)
    # 将数据转换为json格式
    return Response(address)

# 读取商品详情信息
@api_view(['GET'])
def detail(request):
    pass

# 读取商品详情信息(统计)
@api_view(['GET'])
def detail_count(request):
    detail = GoodsDetail.objects.all()
    detail_count = {
        "齿轮减速机": 0,
        "行星减速机": 0,
        "摆线针轮减速机": 0,
    }
    for i in detail:
        if i.type == "齿轮减速机":
            detail_count["齿轮减速机"] += 1
        elif i.type == "行星减速机":
            detail_count["行星减速机"] += 1
        elif i.type == "摆线针轮减速机":
            detail_count["摆线针轮减速机"] += 1
    # 将数据转换为json格式
    return Response(detail_count)


def template(request):
    # 从数据库中读取数据
    goods_info = GoodsInfo.objects.filter(id=1)
    print(goods_info[0].title)
    print(goods_info[0].price)
    # 传递数据到模板
    return render(request, 'sql_data.html')
