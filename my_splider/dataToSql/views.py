from django.shortcuts import render
# from django.http import HttpResponse
from dataToSql.models import GoodsInfo
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
    # 从数据库中读取数据id前10条
    goods_info = GoodsInfo.objects.filter(id__in=[294, 1467, 1993, 2606, 2698])
    # goods_info = GoodsInfo.objects.filter(id=294)
    detail = []
    for i in goods_info:
        # 将数据转换为list
        data = eval(i.detail)
        if len(data) >= 25:
            print(len(data), i.id)
        item = {
            'id': i.id,
            'detail': i.detail,
        }       
        detail.append(item)
    return Response(detail)


def template(request):
    # 从数据库中读取数据
    goods_info = GoodsInfo.objects.filter(id=1)
    print(goods_info[0].title)
    print(goods_info[0].price)
    # 传递数据到模板
    return render(request, 'sql_data.html')
