# Generated by Django 2.2 on 2019-05-08 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0018_auto_20190508_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='camera_name',
            field=models.CharField(default='', max_length=30),
        ),
    ]
