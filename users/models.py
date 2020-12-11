from django.db import models
from datetime import datetime
from hashlib import md5

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField("id", primary_key=True, auto_created=True)
    username = models.CharField('用户名', max_length=50, default='匿名用户', null=False)
    password = models.CharField('密码', max_length=50, null=False)
    email = models.CharField('邮箱', max_length=50, unique=True, null=False)
    is_active = models.BooleanField('是否激活', default=False)
    is_admin = models.BooleanField('超级用户', default=False)
    create_time = models.DateTimeField("创建时间", default=datetime.now())
    def __str__(self):
        return self.username

class Address(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户名")
    address_id = models.IntegerField("id", primary_key=True, auto_created=True)
    telephone = models.CharField("联系电话", max_length=20, null=False)
    is_default_address = models.BooleanField("是否为默认地址", default=False)