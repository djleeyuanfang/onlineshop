# Generated by Django 3.0 on 2019-12-06 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_goodimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodimage',
            name='is_main',
        ),
        migrations.AddField(
            model_name='goodimage',
            name='index',
            field=models.SmallIntegerField(default=0, verbose_name='序号'),
            preserve_default=False,
        ),
    ]