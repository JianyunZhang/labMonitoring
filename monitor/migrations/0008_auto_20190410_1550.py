# Generated by Django 2.2 on 2019-04-10 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_auto_20190410_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='url',
            field=models.CharField(default='', max_length=200),
        ),
    ]