# Generated by Django 3.0 on 2019-12-18 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_report_download_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='complete_time',
            field=models.DateTimeField(null=True, verbose_name='订单成交时间'),
        ),
    ]
