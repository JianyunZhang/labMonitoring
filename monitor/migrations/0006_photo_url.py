# Generated by Django 2.2 on 2019-04-10 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20190410_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='url',
            field=models.CharField(default='', max_length=100),
        ),
    ]