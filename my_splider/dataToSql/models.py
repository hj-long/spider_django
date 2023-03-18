# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class GoodsInfo(models.Model):
    title = models.CharField(blank=True, null=True, max_length=100)
    price = models.CharField(blank=True, null=True, max_length=100)
    sale_sum = models.CharField(blank=True, null=True, max_length=100)
    link = models.CharField(blank=True, null=True, max_length=200)
    detail = models.CharField(blank=True, null=True, max_length=1000)
    address = models.CharField(blank=True, null=True, max_length=200)
    factory_name = models.CharField(blank=True, null=True, max_length=100)
    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'goods_info'

# 新的表，存放GoodsInfo表中的detail字段拆解后的数据
class GoodsDetail(models.Model):
    cross_bag_weight = models.CharField(blank=True, null=True, max_length=100)
    unit_weight = models.CharField(blank=True, null=True, max_length=100)
    orders_goods = models.CharField(blank=True, null=True, max_length=100)
    process = models.CharField(blank=True, null=True, max_length=100)
    num = models.CharField(blank=True, null=True, max_length=100)
    type = models.CharField(blank=True, null=True, max_length=100)
    wheel_type = models.CharField(blank=True, null=True, max_length=100)
    installation = models.CharField(blank=True, null=True, max_length=100)
    layout = models.CharField(blank=True, null=True, max_length=100)
    wheel_hard = models.CharField(blank=True, null=True, max_length=100)
    usage = models.CharField(blank=True, null=True, max_length=100)
    brand = models.CharField(blank=True, null=True, max_length=100)
    type_num = models.CharField(blank=True, null=True, max_length=100)
    input_rev = models.CharField(blank=True, null=True, max_length=100)
    output_rev = models.CharField(blank=True, null=True, max_length=100)
    rating_power = models.CharField(blank=True, null=True, max_length=100)
    allowable_torque = models.CharField(blank=True, null=True, max_length=100)
    use_scope = models.CharField(blank=True, null=True, max_length=100)
    series = models.CharField(blank=True, null=True, max_length=100)
    slow_ratio = models.CharField(blank=True, null=True, max_length=100)
    size = models.CharField(blank=True, null=True, max_length=100)
    sales_area = models.CharField(blank=True, null=True, max_length=100)
    is_brand = models.CharField(blank=True, null=True, max_length=100)
    is_cross = models.CharField(blank=True, null=True, max_length=100)
    speed_ratio_1 = models.CharField(blank=True, null=True, max_length=100)
    speed_ratio_2 = models.CharField(blank=True, null=True, max_length=100)
    speed_ratio_3 = models.CharField(blank=True, null=True, max_length=100)
    # 额定转矩
    rating_torque = models.CharField(blank=True, null=True, max_length=100)
    # 额定转速
    rating_speed = models.CharField(blank=True, null=True, max_length=100)
    # 额定电压
    rating_V = models.CharField(blank=True, null=True, max_length=100)
    # 额定电流
    rating_A = models.CharField(blank=True, null=True, max_length=100)

    # kuajing = models.CharField(blank=True, null=True, max_length=100)
    # danwei_weight = models.CharField(blank=True, null=True, max_length=100)
    # dinghuo = models.CharField(blank=True, null=True, max_length=100)
    # jiagong = models.CharField(blank=True, null=True, max_length=100)
    # num = models.CharField(blank=True, null=True, max_length=100)
    # leibie = models.CharField(blank=True, null=True, max_length=100)
    # chilunleibie = models.CharField(blank=True, null=True, max_length=100)
    # anzhuang = models.CharField(blank=True, null=True, max_length=100)
    # buju = models.CharField(blank=True, null=True, max_length=100)
    # chilunyingdu = models.CharField(blank=True, null=True, max_length=100)
    # yongtu = models.CharField(blank=True, null=True, max_length=100)
    # pinpai = models.CharField(blank=True, null=True, max_length=100)
    # xinghao = models.CharField(blank=True, null=True, max_length=100)
    # shuru = models.CharField(blank=True, null=True, max_length=100)
    # shuchu = models.CharField(blank=True, null=True, max_length=100)
    # endinggonglv = models.CharField(blank=True, null=True, max_length=100)
    # niuju = models.CharField(blank=True, null=True, max_length=100)
    # fanwei = models.CharField(blank=True, null=True, max_length=100)
    # jishu = models.CharField(blank=True, null=True, max_length=100)
    # guige = models.CharField(blank=True, null=True, max_length=100)
    # chukou = models.CharField(blank=True, null=True, max_length=100)
    # jiansubi = models.CharField(blank=True, null=True, max_length=100)
    # chuangdongbi = models.CharField(blank=True, null=True, max_length=100)
    def __str__(self):
        return self.leibie

    class Meta:
        managed = False
        db_table = 'goods_detail'
