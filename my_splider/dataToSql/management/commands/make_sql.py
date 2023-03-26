from django.core.management.base import BaseCommand
from dataToSql.models import GoodsDetail
from dataToSql.views import str_process
import re

class Command(BaseCommand):
    help = 'make sql'
    # 处理命令行参数（可选）
    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    # 处理命令行逻辑
    def handle(self, *args, **options):
        # 从数据库中读取处理数据
        goods_info = GoodsDetail.objects.all()







        # 处理 allowable_torque 的数据
        # for i in goods_info:
        #     allowable_torque = i.allowable_torque
        #     # 如果是空值，直接赋值为0
        #     if not allowable_torque:
        #         i.allowable_torque = 0
        #         i.save()
        #     else:
                # # 正则提取（N.m）前面的数据
                # data = re.findall(r'(.*).N.m', allowable_torque)
                # # 如果有数据，就处理
                # if data:
                #     data = data[0]
                #     # 正则匹配如果出现汉字，就处理成0
                #     if re.search(r'[\u4e00-\u9fa5]', data):
                #         i.allowable_torque = 0
                #     else:
                #         data = data.replace("（N.m）", "")
                #         data = data.replace("(N.m)", "")
                #         data = data.replace("N.m", "")
                #         data = data.replace("N.M", "")
                #         data = data.replace("n.M", "")
                #         data1 = str_process(data)
                #         if data1 != 0:
                #             i.allowable_torque = data1
                #         else:
                #             i.allowable_torque = data
                #     i.save() 
                # 特殊情况处理
                # data = allowable_torque.replace("NM", "")
                # data = data.replace("N.M", "")
                # data = data.replace("N·m", "")
                # data = data.replace("N.m", "")
                # data = data.replace("Nm", "")
                # data = data.replace("Nm", "")
                # data = data.replace("≤", "")
                # data = data.replace("≥", "")
                # data = data.replace("N", "")
                # data1 = str_process(data)
                # if data1 != 0:
                #     i.allowable_torque = data1
                # else:
                #     # 正则判断如果不存在数字0-9，就赋值为0
                #     if not re.search(r'[0-9]', data):
                #         i.allowable_torque = 0
                #     else:
                #         i.allowable_torque = data
                # i.save()


        # 处理rating_power数据，将单位去掉
        # for i in goods_info:
        #     rating_power = i.rating_power
        #     # 如果是空值，直接赋值为0
        #     if not rating_power:
        #         i.rating_power = 0
        #         i.save()
        #     else:
        #         # 正则提取（kw）前面的数据
        #         data = re.findall(r'(.*).kw', rating_power)
        #         # 如果有数据，就处理
        #         if data:
        #             data = data[0]
        #             # 正则匹配如果出现汉字，就处理成0
        #             if re.search(r'[\u4e00-\u9fa5]', data):
        #                 i.rating_power = 0
        #             else:
        #                 data = data.replace("（kw）", "")
        #                 data = data.replace("(kw)", "")
        #                 data = data.replace("kw", "")
        #                 data = data.replace("KW", "")
        #                 i.rating_power = data
        #             i.save()

        # 处理output_rev、input_rev的特殊情况
        # for i in goods_info:
        #     output_rev = i.output_rev
        #     input_rev = i.input_rev
        #     # 把单位rpm或者（rpm）去掉
        #     if output_rev:
        #         output_rev = output_rev.replace("（rpm）", "")
        #         output_rev = output_rev.replace("(rpm)", "")
        #         output_rev = output_rev.replace("rpm", "")
        #         output_rev = output_rev.replace("r/min", "")
        #         output = str_process(output_rev)
        #         if output != 0:
        #             i.output_rev = output
        #         else:
        #             # 正则判断如果不存在数字0-9，就赋值为0
        #             if not re.search(r'[0-9]', output_rev):
        #                 i.output_rev = 0
        #             else:
        #                 i.output_rev = output_rev
        #     if input_rev:
        #         input_rev = input_rev.replace("（rpm）", "")
        #         input_rev = input_rev.replace("(rpm)", "")
        #         input_rev = input_rev.replace("rpm", "")
        #         input_rev = input_rev.replace("r/min", "")
        #         input = str_process(input_rev)
        #         if input != 0:
        #             i.input_rev = input
        #         else:
        #             # 正则判断如果不存在数字0-9，就赋值为0
        #             if not re.search(r'[0-9]', input_rev):
        #                 i.input_rev = 0
        #             else:
        #                 i.input_rev = input_rev
        #     i.save()

        # 处理output_rev数据，将单位去掉
        # for i in goods_info:
        #     output_rev = i.output_rev
        #     # 如果是空值，直接赋值为0
        #     if output_rev == None:
        #         i.output_rev = 0
        #         i.save()
        #     else:
        #         # 正则提取（rpm）前面的数据
        #         data = re.findall(r'(.*).rpm', output_rev)
        #         # 如果有数据，就处理
        #         if data:
        #             data = data[0]
        #             # 正则匹配如果出现汉字，就处理成0
        #             if re.search(r'[\u4e00-\u9fa5]', data):
        #                 i.output_rev = 0
        #             else:
        #                 data = str_process(data)
        #                 if data != 0:
        #                     i.output_rev = data
        #             i.save()
        #         else:
        #             # i.output_rev = 0
        #             # i.save()
        #             pass

        # 处理input_rev数据，将单位去掉
        # for i in goods_info:
        #     input_rev = i.input_rev
        #     # 如果是空值，直接赋值为0
        #     if input_rev == None:
        #         i.input_rev = 0
        #         i.save()
        #     else:
        #         # 正则提取（rpm）前面的数据
        #         data = re.findall(r'(.*).rpm', input_rev)
        #         # 如果有数据，就处理
        #         if data:
        #             data = data[0]
        #             # 正则匹配如果出现汉字，就处理成0
        #             if re.search(r'[\u4e00-\u9fa5]', data):
        #                 i.input_rev = 0
        #             else:
        #                 data = str_process(data)
        #                 if data != 0:
        #                     i.input_rev = data
        #             i.save()
        #         else:
        #             # i.input_rev = 0
        #             # i.save()
        #             pass
        self.stdout.write(self.style.SUCCESS('结束！'))


    # 将上面的单位去除封装成函数
    def unit_remove(str, unit):
        if unit == 'rpm':
            data = re.findall(r'(.*).rpm', str)
        elif unit == 'kw':
            data = re.findall(r'(.*).kw', str)

            if data:
                data = data[0]
                if re.search(r'[\u4e00-\u9fa5]', data):
                    return 0
                else:
                    data = str_process(data)
                    if data != 0:
                        return data
                    else:
                        # 正则判断如果不存在数字0-9，就赋值为0
                        if not re.search(r'[0-9]', data):
                            return 0
                        else:
                            return str
                            
    # 特殊情况处理
    def special_case(str, unit):
        if unit == 'rpm':
            str = str.replace("（rpm）", "")
            str = str.replace("(rpm)", "")
            str = str.replace("rpm", "")
            str1 = str_process(str)
        elif unit == 'kw':
            str = str.replace("（kw）", "")
            str = str.replace("(kw)", "")
            str = str.replace("kw", "")
            str = str.replace("KW", "")
            str1 = str_process(str)
        
            if str1 != 0:
                return str1
            else:
                # 正则判断如果不存在数字0-9，就赋值为0
                if not re.search(r'[0-9]', str):
                    return 0
                else:
                    return str
