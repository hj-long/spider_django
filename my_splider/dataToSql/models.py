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
