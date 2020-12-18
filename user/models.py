from django.db import models
from db.base_model import BaseModel
# from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from hashlib import md5

# Create your models here.
class User( AbstractUser, BaseModel):

    """用户模型类"""
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_active = False
    # user_id = models.IntegerField("id", primary_key=True, auto_created=True)
    def generate_active_token(self):
        '''生成用户名签名字符串'''
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {"confirm": self.user_id}
        token = serializer.dumps(info).decode("utf-8") #解析成字符串
        return token

    user_id = models.AutoField(primary_key=True, verbose_name="id")
    
    # username = models.CharField('用户名', max_length=50, default='匿名用户', null=False)
    # password = models.CharField('密码', max_length=50, null=False)
    # email = models.CharField('邮箱', max_length=50, unique=True, null=False)
    # is_active = models.BooleanField('是否激活', default=False)
    # is_admin = models.BooleanField('超级用户', default=False)
    # create_time = models.DateTimeField("创建时间", default=datetime.now())
    def __str__(self):
        return self.username
    
    class Meta:
        db_table ='df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所属用户")
    receiver = models.CharField(max_length=50, verbose_name="收件人")
    address_id = models.IntegerField( primary_key=True, auto_created=True, verbose_name="id")
    zip_code = models.CharField(max_length=6, null=True, verbose_name="邮政编码")
    telephone = models.CharField( max_length=11, verbose_name="联系电话")
    is_default_address = models.BooleanField( default=False, verbose_name="默认地址")

    class Meta:
        db_table ="df_address"
        verbose_name = "地址"
        verbose_name_plural = verbose_name