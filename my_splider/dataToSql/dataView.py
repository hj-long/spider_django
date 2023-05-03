from dataToSql.models import GoodsInfo, GoodsDetail
from rest_framework.response import Response
from rest_framework.decorators import api_view
import re


# 额定功率与许用扭矩分析
@api_view(['GET'])
def data_view1(request):
    # 获取 JZQ 系列的数据 goodsdetail 表id 0-399 条数据
    goodsdetail = GoodsDetail.objects.filter(id__in=range(0, 400))
    # 获取 JZQ 系列的数据 goodsinfo 表id 0-399 条数据
    goodsinfo = GoodsInfo.objects.filter(id__in=range(0, 400))
    # 满足 power 和 allow_torque 不为空的数据
    goodsdetail = goodsdetail.filter(rating_power__isnull=False, allowable_torque__isnull=False)
    # 返回数据
    data = []
    data1 = {
        '0-10': 0,
        '10-20': 0,
        '20-30': 0,
        '30-40': 0,
        '40-50': 0,
        '50-80': 0,
    }
    power_data = []
    torque_data = []
    for i in range(len(goodsdetail)):
        # 处理范围值 - ~， 无法处理的直接跳过
        i_power = goodsdetail[i].rating_power
        i_allow_torque = goodsdetail[i].allowable_torque
        try:
            if goodsdetail[i].rating_power.find('-') != -1:
                power = goodsdetail[i].rating_power.split('-')
                if float(power[0]) < 1:
                    i_power = float(power[1])
                else:
                    i_power = float(power[0])
            elif goodsdetail[i].rating_power.find('~') != -1:
                power = goodsdetail[i].rating_power.split('~')
                if float(power[0]) < 1:
                    i_power = float(power[1])
                else:
                    i_power = float(power[0])
            else:
                i_power = float(goodsdetail[i].rating_power)
            
            if goodsdetail[i].allowable_torque.find('-') != -1:
                torque = goodsdetail[i].allowable_torque.split('-')
                if float(torque[0]) < 100:
                    i_allow_torque = float(torque[1])
                else:
                    i_allow_torque = float(torque[0])
            elif goodsdetail[i].allowable_torque.find('~') != -1:
                torque = goodsdetail[i].allowable_torque.split('~')
                if float(torque[0]) < 100:
                    i_allow_torque = float(torque[1])
                else:
                    i_allow_torque = float(torque[0])
            else:
                i_allow_torque = float(goodsdetail[i].allowable_torque)
        except:
            continue
        
        # 统计 功率0-10，10-20， 20-30， 30-40，40-50，50-80
        # 单独保存 20-30 的数据
        if i_power >= 20 and i_power < 30:
            # 扭矩超过 10000 的数据算作 10000
            if i_allow_torque > 10000:
                torque_data.append(10000)
            else:
                torque_data.append(i_allow_torque)
            power_data.append(i_power)

        if i_power < 10:
            data1['0-10'] += 1
        elif i_power < 20:
            data1['10-20'] += 1
        elif i_power < 30:
            data1['20-30'] += 1
        elif i_power < 40:
            data1['30-40'] += 1
        elif i_power < 50:
            data1['40-50'] += 1
        elif i_power < 80:
            data1['50-80'] += 1
        
        # 返回数据
        item = {
            'id': goodsdetail[i].id,
            'power': i_power,
            'allow_torque': i_allow_torque,
        }
        data.append(item)

    return Response({'data': 'ok', 'data1': data1, 'power_data': power_data, 'torque_data': torque_data})


# 价格和销量分析
@api_view(['GET'])
def data_view2(request):
    # 获取 JZQ 系列的数据 goodsinfo 表id 0-399 条数据
    goodsinfo = GoodsInfo.objects.filter(id__in=range(0, 400))
    # 满足 price 和 sales 不为空的数据
    goodsinfo = goodsinfo.filter(price__isnull=False, sale_sum__isnull=False)
    # 返回数据
    data = []
    price_data = []
    sales_data = []
    for i in range(len(goodsinfo)):
        # 处理价格 ￥1000
        price = goodsinfo[i].price
        sales = goodsinfo[i].sale_sum
        price = price.replace('￥¥', '')
        price = price.replace('¥', '')
        if '万' in price:
            price = price.replace('万', '')
            price = float(price) * 10000
        else:
            price = float(price)
        # 处理销量 1000+
        if '万' in sales:
            # 提取数字
            sales = re.findall(r"\d+\.?\d*", sales)
            sales = float(sales[0]) * 10000
        else:
            # 提取数字
            sales = re.findall(r"\d+\.?\d*", sales)
            sales = float(sales[0])

        item = {
            'id': goodsinfo[i].id,
            'price': price,
            'sales': sales
        }
        data.append(item)
        # 销量大于0的数据
        if sales > 0:
            price_data.append(price)
            sales_data.append(sales)
        
    return Response({'data': 'ok', 'price_data': price_data, 'sales_data': sales_data})