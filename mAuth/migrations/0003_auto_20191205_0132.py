# Generated by Django 3.0 on 2019-12-05 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mAuth', '0002_auto_20191205_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='上次登录'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=11, verbose_name='手机号'),
        ),
    ]
