import  re

# 
def clear_unit(num, unit):
    # 如果是空值，直接赋值为0
    if num == None:
        return 0
    num = num.strip()
    data = num.replace("（"+unit+"）", "")
    # 正则提取（rpm）前面的数据
    data = re.findall(r'(.*).'+unit, num)
    # 如果有数据，就处理
    if data:
        data = data[0]
        # 正则匹配如果出现汉字，就处理成0
        if re.search(r'[\u4e00-\u9fa5]', data):
            return 0
        else:
            # data = str_process(data)
            if data != 0:
                return data
    else:
        return 0
