# Generated by Django 2.2 on 2019-04-09 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_detection_is_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]