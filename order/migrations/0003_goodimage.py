# Generated by Django 3.0 on 2019-12-06 17:41

from django.db import migrations, models
import django.db.models.deletion
import order.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20191206_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=32, verbose_name='上传原始文件名')),
                ('img', models.ImageField(upload_to=order.models.dre_path, verbose_name='图片路径')),
                ('is_main', models.BooleanField(default=False, verbose_name='主图')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='order.Good', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品图片',
            },
        ),
    ]