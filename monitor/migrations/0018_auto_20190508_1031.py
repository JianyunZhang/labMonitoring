# Generated by Django 2.2 on 2019-05-08 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0017_photo_is_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='is_processed',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='url_processed',
        ),
    ]
