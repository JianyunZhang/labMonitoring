# Generated by Django 2.2 on 2019-05-05 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_assignment_course_instrument_laboratory_select'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='laboratory',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='select',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
