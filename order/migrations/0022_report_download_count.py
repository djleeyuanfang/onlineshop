# Generated by Django 3.0 on 2019-12-15 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_auto_20191215_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='download_count',
            field=models.PositiveIntegerField(default=0, verbose_name='下载次数'),
        ),
    ]