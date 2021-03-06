# Generated by Django 3.0 on 2019-12-06 17:09

from django.db import migrations, models
import order.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimageupload',
            name='file_name',
            field=models.CharField(default='default', max_length=32, verbose_name='上传文件名'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testimageupload',
            name='img',
            field=models.ImageField(upload_to=order.models.dre_path),
        ),
    ]
