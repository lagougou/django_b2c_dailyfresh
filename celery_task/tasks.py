from celery import Celery
from django.core.mail import send_mail
#创建实例类的对象
app = Celery('celery_task.tasks', broker="redis://192.168.18.11:6379/0")

@app.task
def send_email(token, address):
    subject = '新用户激活'
    content = '<a href="http://127.0.0.1:8000/user/active/{}">点击链接激活</a>'.format(token)
    send_mail(subject, '', from_email='jiangruitc@163.com', recipient_list=[address], html_message=content)
