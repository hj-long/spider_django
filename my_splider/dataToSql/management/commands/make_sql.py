from django.core.management.base import BaseCommand
from dataToSql.models import GoodsInfo, GoodsDetail
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
        # 处理input_rev数据，将单位去掉
        for i in goods_info:
            input_rev = i.input_rev
            # 如果是空值，跳过
            if input_rev == None:
                continue
            else:
                data = input_rev.replace("（rpm）", "")
                if data:
                    # 正则匹配如果出现汉字，就处理成0
                    if re.search(r'[\u4e00-\u9fa5]', data):
                        i.input_rev = 0
                    else:
                        data = str_process(data)
                        i.input_rev = data
                    i.save()
                else:
                    i.input_rev = 0
                    i.save()
        self.stdout.write(self.style.SUCCESS('结束！'))