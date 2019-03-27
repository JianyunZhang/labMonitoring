# login/models.py

from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=32, choices=(('male', '男'), ('female', '女'), ), default="男")
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(unique=True, default=13700000000)
    register_time = models.DateTimeField(auto_now_add=True)