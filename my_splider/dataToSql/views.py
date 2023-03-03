# from django.shortcuts import render
# from django.http import HttpResponse
from my_splider.models import GoodsInfo
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
# 从数据库中读取数据, 返回json格式数据
@api_view(['GET'])
def sql_data(request):
    # 从数据库中读取数据
    goods_info = GoodsInfo.objects.all()
    goods = []
    for i in goods_info:
        item = {
            'id': i.id,
            'title': i.title,
            'price': i.price,
            'sale_sum': i.sale_sum,
            'link': i.link,
            'detail': i.detail,
        }
        goods.append(item)
    
    # 将数据转换为json格式
    return Response(goods)









# def sql_data(request):
#     # 从数据库中读取数据
#     goods_info = GoodsInfo.objects.get(id=1)
#     # goods = []
#     # for i in goods_info:
#     #     item = {
#     #         'id': i.id,
#     #         'title': i.title,
#     #         'price': i.price,
#     #         'sale_sum': i.sale_sum,
#     #         'link': i.link,
#     #         'detail': i.detail,
#     #     }
#     #     goods.append(item)
    
#     # 将数据转换为json格式
#     # goods = json.dumps(goods, ensure_ascii=False)
#     # 传递数据到模板
#     return render(request, 'sql_data.html', {'goods': goods_info})
