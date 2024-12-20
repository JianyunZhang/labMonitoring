# Generated by Django 2.2 on 2019-05-04 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_auto_20190409_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.CharField(auto_created=True, max_length=30, primary_key=True, serialize=False)),
                ('student_id', models.CharField(max_length=30)),
                ('student_name', models.CharField(max_length=30)),
                ('course_id', models.CharField(max_length=30)),
                ('course_name', models.CharField(max_length=30)),
                ('teacher_id', models.CharField(max_length=30)),
                ('teacher_name', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=30)),
                ('put_time', models.DateTimeField(auto_now=True)),
                ('file_url', models.CharField(default='', max_length=200)),
                ('score', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(auto_created=True, max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('teacher_id', models.CharField(max_length=30)),
                ('teacher_name', models.CharField(max_length=30)),
                ('laboratory_id', models.CharField(max_length=30)),
                ('laboratory_name', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=30)),
                ('note', models.CharField(max_length=100)),
                ('add_time', models.DateTimeField(auto_now=True)),
                ('file_url', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.CharField(auto_created=True, max_length=30, primary_key=True, serialize=False)),
                ('laboratory_id', models.CharField(max_length=30)),
                ('laboratory_name', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
                ('note', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('photo_url', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.CharField(auto_created=True, max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('department', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=30)),
                ('note', models.CharField(max_length=100)),
                ('photo_url', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Select',
            fields=[
                ('id', models.CharField(auto_created=True, max_length=30, primary_key=True, serialize=False)),
                ('student_id', models.CharField(max_length=30)),
                ('student_name', models.CharField(max_length=30)),
                ('course_id', models.CharField(max_length=30)),
                ('course_name', models.CharField(max_length=30)),
                ('teacher_id', models.CharField(max_length=30)),
                ('teacher_name', models.CharField(max_length=30)),
                ('select_time', models.DateTimeField(auto_now=True)),
                ('score', models.CharField(max_length=10)),
            ],
        ),
    ]
