# Generated by Django 3.0 on 2019-12-08 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20191208_1242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='ImageDir',
            new_name='image_dir',
        ),
    ]
