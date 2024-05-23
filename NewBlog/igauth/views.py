from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.db import connection
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User

User = get_user_model()


# Create your views here.
@require_http_methods(['GET', 'POST'])
def iglogin(request):
    if request.method == 'GET':
        return render(request, 'html/login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # 登录
                login(request, user)
                # 判断是否需要记住我
                if not remember:
                    # 如果没有点击记住我，那么就要设置过期时间为0，即浏览器关闭后就会过期
                    request.session.set_expiry(0)
                # 如果点击了，就什么都不会做，默认在两周的情况下信息过期
                request.session.set_expiry(1000000)
                return redirect('/')
            else:
                print("邮箱或者密码错误！")
                # form.add_error('email', '邮箱或者密码错误！')
                # return render(request, 'html/login.html', context={"form": form})
                return redirect(reverse('login'))


def iglogout(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'html/register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('login'))
        else:
            print(form.errors)
            # 重新跳转到
            return redirect(reverse('register'))


def send_email_captcha(request):
    # ?email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": '必须传递邮箱！'})
    # 生成验证码（随机取四位阿拉伯数字）
    captcha = "".join(random.sample(string.digits, 4))
    # 存储到数据库中
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail("IGOR博客注册验证码", message=f"您的注册验证码是:{captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({"code": 200, "message": "邮箱验证码发送成功"})
