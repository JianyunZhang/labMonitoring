# Generated by Django 2.2 on 2019-05-08 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0016_remove_photo_is_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='is_phone',
            field=models.BooleanField(default=None),
        ),
    ]