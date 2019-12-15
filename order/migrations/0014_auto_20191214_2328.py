# Generated by Django 3.0 on 2019-12-14 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_auto_20191214_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='is_edit',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('SUMMIT', '订单已提交，待付款'), ('PAY', '订单已付款，待发货'), ('SHIP', '订单运送中，待收货'), ('COMPLETE', '订单完成'), ('CANCEL', '交易关闭')], default='SUMMIT', max_length=10, verbose_name='订单状态'),
        ),
    ]
