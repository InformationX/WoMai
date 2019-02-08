from django.db import models

# Create your models here.

# 用户
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.username

# 商品
class Goods(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    picture = models.FileField(upload_to='./upload/')
    desc = models.TextField()

    def __str__(self):
        return self.name