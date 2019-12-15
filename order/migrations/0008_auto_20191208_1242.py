# Generated by Django 3.0 on 2019-12-08 12:42

from django.db import migrations, models
import django.db.models.deletion
import order.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20191207_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageDir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(max_length=50, unique=True, verbose_name='分类目录')),
            ],
        ),
        migrations.RemoveField(
            model_name='goodimage',
            name='img',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=32, verbose_name='上传文件名')),
                ('img', models.ImageField(upload_to=order.models.dre_path)),
                ('ImageDir', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='order.ImageDir', verbose_name='目录')),
            ],
        ),
        migrations.AddField(
            model_name='goodimage',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='order.Image', verbose_name='图片'),
        ),
    ]