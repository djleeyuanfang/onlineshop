# Generated by Django 3.0 on 2019-12-08 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20191208_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='is_show',
            field=models.BooleanField(default=True, verbose_name='显示在面板上面'),
        ),
    ]
