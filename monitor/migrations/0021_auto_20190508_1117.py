# Generated by Django 2.2 on 2019-05-08 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0020_setting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='user_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='setting',
            name='user_name',
            field=models.CharField(max_length=30),
        ),
    ]
