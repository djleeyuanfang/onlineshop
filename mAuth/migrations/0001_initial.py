# Generated by Django 3.0 on 2019-12-04 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('mail', models.CharField(max_length=50, unique=True, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('is_active', models.BooleanField(default=True, verbose_name='有效')),
                ('is_admin', models.BooleanField(default=False, verbose_name='管理员')),
                ('last_login', models.DateTimeField(verbose_name='上次登录')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
            ],
            options={
                'verbose_name': '用户',
            },
        ),
        migrations.CreateModel(
            name='MailCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.CharField(max_length=50, unique=True, verbose_name='邮箱')),
                ('code', models.CharField(max_length=6, verbose_name='验证码')),
                ('create_time', models.DateTimeField(verbose_name='验证码时间')),
            ],
            options={
                'verbose_name': '邮箱验证码',
            },
        ),
    ]