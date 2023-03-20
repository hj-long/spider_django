from django.shortcuts import render
# from django.http import HttpResponse
from dataToSql.models import GoodsInfo, GoodsDetail
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count

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

# 读取城市信息进行返回统计结果
@api_view(['GET'])
def address(request):
    info = GoodsInfo.objects.all()
    address_count = {}
    for i in info:
        # 对address属性进行分割提取，再进行统计
        address = i.address.split(" ")
        if len(address) < 2:
            print(i.id, '地址信息不完整')
        else:
            city = address[1]
            if city in address_count:
                address_count[city] += 1
            else:
                address_count[city] = 1
    return Response(headers={'Access-Control-Allow-Origin': '*'}, data=address_count)
    # return Response(address_count)

# 根据参数统计返回一个范围内的数据
@api_view(['GET'])
def info_data(request):
    # 读取一定范围的额定功率
    power_num = 200
    info = GoodsDetail.objects.filter(rating_power__range=[power_num-100, power_num+100])
    info_data = []
    for i in info:
        power = i.rating_power
        num = power.replace("（kw）", "")
        if len(num) >= len(str(power_num-100)):
            item = {
                'id': i.id,
                'rating_power': num,
                'type': i.type,
            }
            info_data.append(item)
    return Response(headers={'Access-Control-Allow-Origin': '*'}, data=info_data)

    
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
    return Response(headers={'Access-Control-Allow-Origin': '*'}, data=detail_count)


def template(request):
    # 从数据库中读取数据
    goods_info = GoodsInfo.objects.filter(id=1)
    print(goods_info[0].title)
    print(goods_info[0].price)
    # 传递数据到模板
    return render(request, 'sql_data.html')
