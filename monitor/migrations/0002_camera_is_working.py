# Generated by Django 2.2 on 2019-04-09 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='is_working',
            field=models.BooleanField(default=False),
        ),
    ]
