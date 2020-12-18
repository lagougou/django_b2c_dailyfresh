from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User
from django.views.generic import TemplateView
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import re
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core.mail import send_mail
from celery_task.tasks import send_email
from django.contrib.auth.decorators import login_required
from utils.minxin import LoginRequiredMixin

# Create your views here.
def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    else:
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'user/register.html', {'errmsg': '数据不完整'})

        # 检验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'user/register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'user/register.html', {'errmsg': '请同意协议'})

        # 校验用户是否重复
        try:
            user = User.objects.get(username=username)
        except Exception:
            # 用户名不存在
            user = None

        if user:
            return render(request, 'user/register.html', {'errmsg': '用户已存在'})

        # 进行业务处理：进行用户注册
        user = User.objects.create_user(username, email, password)
        # user.is_active = 0
        user.save()
        
        # 返回应答,跳转首页
        return redirect(reverse('goods:index'))

# def send_email(token,addr):
            
#     subject = '新用户激活'
#     content = '<a href="http://127.0.0.1:8000/user/active/{}">点击链接激活</a>'.format(token)
#     send_mail(subject, '', from_email='jiangruitc@163.com', recipient_list=[addr], html_message=content)

class RegiterView(TemplateView):
    # template_name = 'user/regiter.html'
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'user/register.html', {'errmsg': '数据不完整'})

        # 检验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'user/register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'user/register.html', {'errmsg': '请同意协议'})

        # 校验用户是否重复
        try:
            user = User.objects.get(username=username)
        except Exception:
            # 用户名不存在
            user = None

        if user:
            return render(request, 'user/register.html', {'errmsg': '用户已存在'})

        # 进行业务处理：进行用户注册
        user = User.objects.create_user(username, email, password)
        # user.is_active = 0
        user.save()
        if not user.is_active:
            token = user.generate_active_token()
            send_email.delay(token, user.email)
            # subject = '新用户激活'
            # content = '<a href="http://127.0.0.1:8000/activen/{}">点击链接激活</a>'.format(token)
            # send_mail(subject, content, from_email='jiangruitc@163.com', recipient_list=[user.email])
            return redirect(reverse('user:login'))
        # 返回应答,跳转首页
        return redirect(reverse('goods:index'))

# class EmailView(TemplateView):
#     template_name = 'auth.html'
#     def get(self, request, user, token):
#         return render(request, self.template_name, {"user": user, "token": token} )

class ActiveView(TemplateView):
    template_name = 'user/active.html'
    def get(self, request, token):
        #解密 获取要激活的用户信息
        seris = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = seris.loads(token)
            user_id = info.get('confirm')
            user = User.objects.get(user_id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            print(e)
            return HttpResponse("激活链接已经过期")

class LoginView(TemplateView):

    template_name = 'user/login.html'
    def get(self, request):
        print(self.template_name)
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # print(username, password)
        if not all([username, password]):
            return render(request, self.template_name, {'errmsg': '数据不完整'})

    #业务处理校验
        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            return render(request, self.template_name, {"errmsg": "用户或密码不正确"})
        else:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', reverse('good:index'))
                
                return redirect(reverse(next_url))
            return render(request,self.template_name, {"errmsg": "用户未激活"})


class UserCenterView(LoginRequiredMixin):
    """用户中心"""
    template_name = 'user/center.html'
   
    def get(self, request):
        '''显示'''
        return render(request,self.template_name )


class UserOrderView(LoginRequiredMixin,TemplateView):
    template_name = 'user/order.html'
    @login_required
    def get(self, request):
        return render(self, 'user/order.html')


class UserAddressView(LoginRequiredMixin, TemplateView):
    template_name = 'user/addr.html'
    @login_required
    def get(self, request):
        return render(self, 'user/addr.html')