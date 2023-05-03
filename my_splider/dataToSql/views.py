from django.shortcuts import render
from dataToSql.models import GoodsInfo, GoodsDetail
from rest_framework.response import Response
from rest_framework.decorators import api_view
import wordcloud
import jieba
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re



# Create your views here.
# 从数据库中读取数据, 返回json格式数据
@api_view(['GET'])
def sql_data(request):
    # 从数据库中读取数据id前100条
    goods_info = GoodsInfo.objects.filter(id__lte=100)
    goods = []
    # 分页
    paginator_obj = Paginator(goods_info, 10)
    page = request.GET.get('page')
    goods_info = paginator_obj.get_page(page)
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
    return Response(data=address_count)

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
        "圆柱齿轮减速机": 0,
        "摆线针轮减速机": 0,
        "圆锥齿轮减速机": 0,
        "行星齿轮减速机": 0,
        '其他类型': 0,
    }
    for i in detail:
        data = i.wheel_type
        if data != None:
            if "圆" in data:
                detail_count["圆柱齿轮减速机"] += 1
            elif "针轮" in data:
                detail_count["摆线针轮减速机"] += 1
            elif "锥" in data:
                detail_count["圆锥齿轮减速机"] += 1
            elif "行星" in data:
                detail_count["行星齿轮减速机"] += 1
            elif "斜" in data:
                detail_count["圆锥齿轮减速机"] += 1
            else:
                detail_count["其他类型"] += 1
        else:
            detail_count["其他类型"] += 1

    data = [
        {"name": "圆柱齿轮减速机", "value": detail_count["圆柱齿轮减速机"]},
        {"name": "摆线针轮减速机", "value": detail_count["摆线针轮减速机"]},
        {"name": "圆锥齿轮减速机", "value": detail_count["圆锥齿轮减速机"]},
        {"name": "行星齿轮减速机", "value": detail_count["行星齿轮减速机"]},
        {"name": "其他类型", "value": detail_count["其他类型"]},
        ]
    length = len(detail)
    # 将数据转换为json格式
    return Response(data={"data": data, "length": length})


def template(request):
    # 从数据库中读取数据
    goods_info = GoodsInfo.objects.filter(id=1)
    print(goods_info[0].title)
    print(goods_info[0].price)
    # 传递数据到模板
    return render(request, 'sql_data.html')


# 返回词云图片
@api_view(['GET'])
def word_cloud(request):
    # 读取数据库中所有的 use_scope 字段的数据
    data = GoodsDetail.objects.values_list('use_scope')
    
    # 读取数据
    text = ""
    for item in data:
        if item[0] is not None:
            # item[0]格式为 食品、纺织、冶金 或者 撕碎机,皮带机，矿山设备，电厂，水泥厂 需要去除逗号和数字，并且分词
            if item[0].isdigit():
                continue
            text += ' '.join(jieba.cut(item[0].replace(',', '').replace('，', '').
                                       replace('、', '').replace('等行业', '').replace('等领域', '').replace('等', '').
                                            replace('等', '').replace(' ', '').replace('（', '').replace('）', '').
                                                replace('(', '').replace(')', '')))
    # 生成词云
    wc = wordcloud.WordCloud(
        font_path='C:\Windows\Fonts\simhei.ttf', width=1000, height=800, background_color='white',
        collocations=False
    )
    wc.generate(text)
    # 保存图片
    wc.to_file('upload/word_cloud.png')
    # 返回图片地址
    return Response(data='http://127.0.0.1:8000/upload/word_cloud.png')

# 搜索功能
@api_view(['GET'])
def search(request):
    # 获取搜索关键字
    name = request.GET.get('name')  or ""
    type = request.GET.get('type') or ""
    factory = request.GET.get('factory') or ""
    series = request.GET.get('series')  or ""
    use_scope = request.GET.get('use_scope') or ""
    address = request.GET.get('address')    or ""
    # 获取页码
    page = request.GET.get('page')
    # 获取每页显示的数量
    page_size = request.GET.get('page_size')
    # 根据关键字查询
    if name != "":
        goods_info = GoodsInfo.objects.filter(title__contains=name)
    if type != "":
        goods_info = GoodsDetail.objects.filter(type_num__contains=type)
    if factory != "":
        goods_info = GoodsInfo.objects.filter(factory_name__contains=factory)
    if series != "":
        goods_info = GoodsDetail.objects.filter(series__contains=series)
    if use_scope != "":
        goods_info = GoodsDetail.objects.filter(use_scope__contains=use_scope)
    if address != "":
        goods_info = GoodsInfo.objects.filter(address__contains=address)
    # 分页
    paginator = Paginator(goods_info, page_size)
    # 获取第page页的内容
    page_obj = paginator.get_page(page)
    # 获取当前页码
    current_page = page_obj.number
    # 获取当前页码的数据
    data = page_obj.object_list
    # 获取总页数
    total_page = paginator.num_pages
    # 获取总数据量
    total_count = paginator.count
    # 将数据转换为json格式
    res_data = []
    for i in data:
        detail = GoodsDetail.objects.get(id=i.id)
        info = GoodsInfo.objects.get(id=i.id)
        item = {
            "id": i.id,
            "title": info.title,
            "price": info.price,
            "address": info.address.replace('中国 ', ''),
            "factory_name": info.factory_name,
            "type": detail.type_num,
            "series": detail.series,
            "use_scope": detail.use_scope,
            "link": info.link,
            "wheel_type": detail.wheel_type,
        }
        res_data.append(item)

    return Response(data={"data": res_data, "current_page": current_page, "total_page": total_page, "total_count": total_count})


# 智能推荐
@api_view(['GET'])
def recommend(request):
    # 获取搜索关键字
    power = request.GET.get('power') or ""
    input_rev = request.GET.get('input_rev') or ""
    output_rev = request.GET.get('output_rev') or ""
    allow_torque = request.GET.get('allow_torque') or ""
    slow_ratio = request.GET.get('slow_ratio') or ""
    series = request.GET.get('series') or ""

    # 先根据series查询,再根据其他参数查询
    if series != "":
        goods_info = GoodsDetail.objects.filter(series__contains=series)
    else:
        return Response('can not find series')

    # 整理数据
    data = []
    for i in goods_info:
        # 得分
        score = 0

        info = GoodsInfo.objects.get(id=i.id)
        # 判断 power 是否在范围内
        if power != "":
            power = float(power)
            _p = i.rating_power        
            if _p != '':
                if is_in_range(power, _p, 5, 5) is False:
                    continue
                else:
                    score += 1
            elif _p == '0':
                score -= 0.5

        # 判断 input_rev 是否在范围内
        if input_rev != "":
            input_rev = float(input_rev)
            _i = i.input_rev
            if _i != '':
                if is_in_range(input_rev, _i, 100, 100) is False:
                    continue
                else:
                    score += 1
            elif _i == '0':
                score -= 0.5

        # 判断 output_rev 是否在范围内
        if output_rev != "":
            output_rev = float(output_rev)
            _o = i.output_rev
            if _o != '':
                if is_in_range(output_rev, _o, 30, 30) is False:
                    continue
                else:
                    score += 1
            elif _o == '0':
                score -= 0.5

        # 判断 allow_torque 是否在范围内
        if allow_torque != "":
            allow_torque = float(allow_torque)
            _a = i.allowable_torque
            if _a != '':
                if is_in_range(allow_torque, _a, 100, 100) is False:
                    continue
                else:
                    score += 1
            elif _a == '0':
                score -= 0.5

        # 判断 slow_ratio 是否在范围内
        if slow_ratio != "":
            slow_ratio = float(slow_ratio)
            _s = i.slow_ratio
            if _s != '':
                if is_in_range(slow_ratio, _s, 5, 5) is False:
                    continue
                else:
                    score += 1
            elif _s == '0':
                score -= 0.5

        # 计算价格和销售量得分
        if info.price != '':
            price = info.price
            price = price.replace('￥', '')
            price = price.replace('¥', '')
            if '万' in price:
                score += 5
            else:
                # 提取数字
                price = re.findall(r"\d+\.?\d*", price)
                price = float(price[0])
                if 0.01 * price < 1:
                    score += 1
                else:
                    score += 2
        if info.sale_sum != '' and info.sale_sum != '0':
            sale = info.sale_sum
            # 提取数字
            if '万' in sale:
                sale = re.findall(r"\d+\.?\d*", sale)
                sale = float(sale[0])
                score += sale
            else:
                sale = re.findall(r"\d+\.?\d*", sale)
                sale = float(sale[0])
                if 0.01 * sale < 1:
                    score += 1
                else:
                    score += 2
            
        item = {
            "id": i.id,
            "price": info.price,
            "sale_sum": info.sale_sum,
            "power": i.rating_power,
            "input_rev": i.input_rev,
            "output_rev": i.output_rev,
            "allow_torque": i.allowable_torque,
            "slow_ratio": i.slow_ratio,
            "series": i.series,
            "type": i.type_num,
            "wheel_hard": i.wheel_hard,
            "layout": i.layout,
            "installation": i.installation,
            "score": format(score, '.2f')
        }
        data.append(item)
    # 按得分排序
    data = sorted(data, key=lambda x: x['score'], reverse=True)
    # 如果参数 flag 为 1，返回前 15 条数据
    flag = request.GET.get('flag') or ""
    if flag == '1':
        data = data[:15]
        # 统计power、input_rev、output_rev、id
        power_list = []
        input_rev_list = []
        output_rev_list = []
        num_list = []
        for i in data:
            power1 = i['power']
            input_rev1 = i['input_rev']
            output_rev1 = i['output_rev']
            power_list.append(to_OK(power1, power))
            input_rev_list.append(to_OK(input_rev1, input_rev))
            output_rev_list.append(to_OK(output_rev1, output_rev))
            num_list.append(i['id'])
        return Response(data={"data":data, "power":power_list, "input_rev":input_rev_list, "output_rev":output_rev_list, "num":num_list})

    else: 
        return Response(data={"data":data})

# 数字正常处理
def to_OK(data, num=0):
    if data != '' and data is not None:
        try:
            data = float(data)
            return data
        except:
            if '-' in data:
                data = data.split('-')
                if float(data[0]) < 1:
                    if num > 0:
                        return num
                    else:
                        return data[1]
                else:
                    return float(data[0])
            elif '~' in data:
                data = data.split('~')
                if float(data[0]) < 1:
                    if num > 0:
                        return num
                    else:
                        return data[1]
                else:
                    return float(data[0])
    return float(data)

# 判断是否在范围内 data:参数数字 value:数据库字段值字符串 min: 最小范围 max: 最大范围
def is_in_range(data, value, min=0, max=0):
    # 判断 value 是否是数字，如果不是数字，可能是范围值，如果不是数字也不是范围值，直接返回 False
    if value is not None:
        try:
            value = float(value)
            # 判断 value 是否在范围内
            if data - min > value or data + max < value:
                return False
        except:
            # 看看是否为范围值，如 0.75-1.5、0.75~1.5
            if '-' in value:
                value = value.split('-')
                if data >= float(value[1]) or data <= float(value[0]):   
                    return False
            elif '~' in value:
                value = value.split('~')
                if data >= float(value[1]) or data <= float(value[0]):   
                    return False
            else:
                return False
    else:
        return False
    return True

