# Generated by Django 2.1.7 on 2019-03-28 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20190328_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.IntegerField(default=0, max_length=30),
        ),
    ]
