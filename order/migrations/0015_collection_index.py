# Generated by Django 3.0 on 2019-12-15 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20191214_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='index',
            field=models.SmallIntegerField(default=0, verbose_name='顺序'),
            preserve_default=False,
        ),
    ]
