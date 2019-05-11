# Generated by Django 2.2 on 2019-05-08 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0011_camera_photo_quality'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='is_detected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='photo',
            name='is_phone',
            field=models.BooleanField(default=None),
        ),
        migrations.AddField(
            model_name='photo',
            name='is_predicted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='photo',
            name='list_predicted',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='photo',
            name='url_detected',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='camera',
            name='photo_quality',
            field=models.IntegerField(default=100),
        ),
    ]