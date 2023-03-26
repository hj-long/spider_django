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

# 根据参数统计返回一个范围内的额定功率
@api_view(['GET'])
def g_power(request):
    # 读取一定范围的额定功率
    power = request.GET.get('power')
    if power == None:
        power = 200
    info = GoodsDetail.objects.filter(rating_power__range=[power-100, power+100])
    info_data = []
    for i in info:
        data = i.rating_power
        # 对数据字符串进行处理
        num = data.replace("（kw）", "")
        num = str_process(num)
        if num and num >= (power-100) and num <= (power+100):
            item = {
                'id': i.id,
                'rating_power': num,
                'type': i.type,
            }
            info_data.append(item)
    return Response(headers={'Access-Control-Allow-Origin': '*'}, data=info_data)

# 对数据字符串进行处理
def str_process(str):
    flag = True
    # 去除空格
    num = str.replace(" ", "")
    # 如果有-或者~或者/或者、，则取中间值
    try:
        if "-" in num:
            num = num.split("-")
            # 如果只有一个值，则取这个值
            if num[0] == "":
                num = float(num[1])
            else:
                num = (float(num[0]) + float(num[1])) / 2
        elif "~" in num:
            num = num.split("~")
            num = (float(num[0]) + float(num[1])) / 2
        elif "/" in num:
            num = num.split("/")
            if num[0] == "":
                num = float(num[1])
            num = (float(num[0]) + float(num[1])) / 2
        elif "、" in num:
            num = num.split("、")
            num = (float(num[0]) + float(num[1])) / 2
        # 如果有 > 或者 < 则取后面的值
        elif ">" in num:
            num = num.split(">")
            num = float(num[1])
        elif "<" in num:
            num = num.split("<")
            num = float(num[1])
        # 转为int类型，失败就是有字母
        num = int(num)
    except:
        flag = False
    if flag :
        return num
    else:
        return 0

# 获取输入转速
@api_view(['GET'])
def g_inputRev(request):
    # 获取参数
    speed = request.GET.get('input_rev')
    if speed == None:
        speed = 1000
    info = GoodsDetail.objects.filter(input_rev__range=[1, speed+500])
    info_data = []
    for i in info:
        data = i.input_rev
        # 对数据字符串进行处理
        num = data.replace("（rpm）", "")
        num = str_process(num)
        if num and num >= (speed-500) and num <= (speed+500):
            item = {
                'id': i.id,
                'output_speed': num,
                'type': i.type,
            }
            info_data.append(item)
    return Response(headers={'Access-Control-Allow-Origin': '*'}, data=info_data)

# 获取输出转速
@api_view(['GET'])
def g_outputRev(request):
    # 获取参数
    speed = request.GET.get('output_rev')
    if speed == None:
        speed = 500
    info = GoodsDetail.objects.filter(output_rev__range=[speed-100, speed+200])
    info_data = []
    for i in info:
        data = i.output_rev
        # 对数据字符串进行处理
        num = data.replace("（rpm）", "")
        num = str_process(num)
        if num and num >= (speed-100) and num <= (speed+200):
            item = {
                'id': i.id,
                'output_speed': num,
                'type': i.type,
            }
            info_data.append(item)
    return Response(headers={'Access-Control-Allow-Origin': '*'}, data=info_data)

# 获取许用扭矩
@api_view(['GET'])
def g_torque(request):
    # 获取参数
    torque = request.GET.get('torque')
    if torque == None:
        torque = 100
    info = GoodsDetail.objects.filter(allowable_torque__range=[1, torque+200])
    info_data = []
    for i in info:
        data = i.allowable_torque
        # 对数据字符串进行处理
        num = data.replace("（N.m）", "")
        num = str_process(num)
        if num and num >= (torque-50) and num <= (torque+1000):
            item = {
                'id': i.id,
                'torque': num,
                'type': i.type,
            }
            info_data.append(item)
    return Response(headers={'Access-Control-Allow-Origin': '*'}, data=info_data)


# 获取减速比
@api_view(['GET'])
def g_ratio(request):
    # 获取参数
    ratio = request.GET.get('ratio')
    if ratio == None:
        ratio = 10
    info = GoodsDetail.objects.filter(slow_ratio__range=[1, ratio+5])
    info_data = []
    for i in info:
        data = i.slow_ratio
        # 对数据字符串进行处理
        if data != None:
            try:
                num = int(data)
            except:
                num = 0
            if num and num >= (ratio-5) and num <= (ratio+5):
                item = {
                    'id': i.id,
                    'ratio': num,
                    'type': i.type,
                }
                info_data.append(item)
    return Response(headers={'Access-Control-Allow-Origin': '*'}, data=info_data)



# 读取商品详情信息(统计)
@api_view(['GET'])
def detail_count(request):
    detail = GoodsDetail.objects.all()
    detail_count = {
        "行星减速机": 0,
        "摆线针轮减速机": 0,
        "蜗轮蜗杆减速机": 0,
        '其他类型': 0,
    }
    for i in detail:
        data = i.type
        if data:
            if "蜗轮" in i.type or "蜗杆" in i.type:
                detail_count["蜗轮蜗杆减速机"] += 1
            elif "摆线" in i.type or "针轮" in i.type:
                detail_count["摆线针轮减速机"] += 1
            elif "齿轮减" in i.type or "行星" in i.type:
                detail_count["行星减速机"] += 1
            else:
                detail_count["其他类型"] += 1
        else:
            detail_count["其他类型"] += 1

    data = [
            { "name": "行星减速机", "value": detail_count["行星减速机"] },
            { "name": "摆线针轮减速机", "value": detail_count["摆线针轮减速机"] },
            { "name": "蜗轮蜗杆减速机", "value": detail_count["蜗轮蜗杆减速机"] },
            { "name": "其他类型", "value": detail_count["其他类型"] }
        ]
    length = len(detail)
    # 将数据转换为json格式
    return Response(headers={'Access-Control-Allow-Origin': '*'}, data={"data": data, "length": length})


def template(request):
    # 从数据库中读取数据
    goods_info = GoodsInfo.objects.filter(id=1)
    print(goods_info[0].title)
    print(goods_info[0].price)
    # 传递数据到模板
    return render(request, 'sql_data.html')
