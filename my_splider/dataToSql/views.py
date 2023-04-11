from django.shortcuts import render
# from django.http import HttpResponse
from dataToSql.models import GoodsInfo, GoodsDetail
# import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from django.db.models import Count

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

@api_view(['GET'])
def get_data(request):
    # 获取参数
    param = request.GET
    if param == None or len(param) > 1:
        return Response('参数错误')
    
    # 参数处理范围
    val = 0
    name = ''
    # 读取参数
    for i in param:
        print(i, param[i])
        if i == 'power':
            power = param[i]
            # 读取一定范围的额定功率
            val = int(power)
            name = 'rating_power'
        elif i == 'input_rev':
            input_rev = param[i]
            # 读取一定范围的额定输入转速
            val = int(input_rev)
            name = 'input_rev'
    
    infos = GoodsDetail.objects.all()
    info_data = []
    for i in infos:
        if name == 'rating_power':
            try:
                rating_power = float(i.rating_power)
                if rating_power >= (val-5) and rating_power <= (val+5):
                    good = GoodsInfo.objects.get(id=i.id)
                    item = {
                        "id": i.id,
                        "power_data": i.rating_power,
                        "input_rev": i.input_rev,
                        "output_rev": i.output_rev,
                        "slow_ratio": i.slow_ratio,
                        "sale_sum": good.sale_sum,
                        "price": good.price,
                    }
                    info_data.append(item)
            except:
                pass

    # 对数据进行统计 {
    #   "power_data": {
    #       "0-5": 0,
    #       "5-10": 0,
    #       "10-15": 0,
    #    },
    #   ....
    # }
    count_data = {
        "额定功率": {},
        "输入转速": {},
        "输出转速": {},
        "减速比": {},
        "价格": {},
    }

    for i in info_data:
        power_data = i['power_data']
        input_rev = i['input_rev']
        output_rev = i['output_rev']
        slow_ratio = i['slow_ratio']
        sale_sum = i['sale_sum']
        # 对额定功率进行统计
        if power_data != None:
            count_data['额定功率'][power_data] = count_data['额定功率'].get(power_data, 0) + 1
        # 对输入转速进行统计
        if input_rev != None:
            count_data['输入转速'][input_rev] = count_data['输入转速'].get(input_rev, 0) + 1
        # 对输出转速进行统计
        if output_rev != None:
            count_data['输出转速'][output_rev] = count_data['输出转速'].get(output_rev, 0) + 1
        # 对减速比进行统计
        if slow_ratio != None:
            count_data['减速比'][slow_ratio] = count_data['减速比'].get(slow_ratio, 0) + 1
        # 对价格进行统计
        if sale_sum != None:
            if sale_sum == '0':
                sale_sum = '成交0+元'
            count_data['价格'][sale_sum] = count_data['价格'].get(sale_sum, 0) + 1

    return Response({
        'data': info_data,
        'count': count_data,
    })

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
