# Generated by Django 3.0 on 2019-12-14 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_goodtrack'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ship_time',
            field=models.DateTimeField(null=True, verbose_name='订单发货时间'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('SUMMIT', '订单已提交，待付款'), ('PAY', '订单已付款'), ('SHIP', '订单运送中'), ('COMPLETE', '订单完成'), ('CANCEL', '交易关闭')], default='SUMMIT', max_length=10, verbose_name='订单状态'),
        ),
    ]
