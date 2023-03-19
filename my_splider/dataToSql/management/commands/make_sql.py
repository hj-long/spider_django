from django.core.management.base import BaseCommand
from dataToSql.models import GoodsInfo, GoodsDetail

class Command(BaseCommand):
    help = 'make sql'
    # 处理命令行参数（可选）
    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    # 处理命令行逻辑
    def handle(self, *args, **options):
        # 从数据库中读取数据id前10条
        goods_info = GoodsInfo.objects.filter(id__lte=10)
        goods = []
        name_list = {
            '跨境包裹重量': 'cross_bag_weight', '单位重量': 'unit_weight', '订货号': 'orders_goods',
            '加工定制': 'process','货号': 'num', '类别': 'type', 
            '齿轮类型': 'wheel_type', '安装形式': 'installation','布局形式': 'layout', 
            '齿面硬度': 'wheel_hard', '用途': 'usage', '品牌': 'brand', 
            '型号': 'type_num','输入转速': 'input_rev', '输出转速范围': 'output_rev', 
            '额定功率': 'rating_power', '许用扭矩': 'allowable_torque', '使用范围': 'use_scope',
            '额定电压': 'rating_V', '额定电流': 'rating_A', '额定转速': 'rating_speed', 
            '额定转矩': 'rating_torque', '级数': 'series', '减速比': 'slow_ratio', 
            '规格': 'size', '主要销售地区': 'sales_area', '有可授权的自有品牌': 'is_brand', '是否跨境出口专供货源': 'is_cross',
        }
        for info in goods_info:
            # 将数据转换为list
            detail_list = eval(info.detail)
            goods_detail = GoodsDetail()
            for item in detail_list:
                # 判断是否有该属性
                if name_list.get(item['name']) is not None and hasattr(goods_detail, name_list[item['name']]):
                    print('找到属性：', name_list[item['name']], item['value'])
                    # 将数据写入数据库,循环写入属性
                    setattr(goods_detail, name_list[item['name']], item['value'])
            goods_detail.save()
        self.stdout.write(self.style.SUCCESS('结束！'))