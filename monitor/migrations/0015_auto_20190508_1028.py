# Generated by Django 2.2 on 2019-05-08 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0014_auto_20190508_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='is_phone',
            field=models.CharField(default='', max_length=10),
        ),
    ]
