# Generated by Django 2.2 on 2019-05-08 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0021_auto_20190508_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='detection_model',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='photo',
            name='prediction_model',
            field=models.CharField(default='', max_length=30),
        ),
    ]