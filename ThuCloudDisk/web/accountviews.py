# This Python file uses the following encoding: utf-8
from django import forms
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login,logout as auth_logout
from web.models import MyUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def register(request):
    auth_logout(request)
    return render(request,'accounts/register.html')

@csrf_protect
def register_do(request):
    auth_logout(request)
    try:
        email = request.POST['email']
        password = request.POST['password']
        nickname = request.POST['nickname']
        password_confirm = request.POST['password_confirm']
    except:
        return redirect('/register')
    try:
        MyUser.objects.get(email=email)
        emailExist = True
        return render(request,"accounts/register.html",locals())
    except MyUser.DoesNotExist:
        user = MyUser.objects.create_user(email = email, nickname = nickname, password = password)
        user.save()
        user = authenticate(email = email, password = password)
        auth_login(request,user)
        return redirect("/home/files?firstLogin=True")
def check_email(request):
    email = request.GET['email']
    try:
        MyUser.objects.get(username=username)
        return ('exist')
    except MyUser.DoesNotExist:
        return ('not_exist')
    return ('not_exist')
@csrf_protect
def login(request): 
    if request.user.is_authenticated():
        return redirect('/home/files')
    if 'next' in request.GET:
        next = request.GET['next']
    else: next='/'
    if 'email' in request.GET:
        email = request.GET['email']
    return render(request,'accounts/login.html',locals())

@csrf_protect
def login_do(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
        next = request.POST['next']
    except:
        return redirect('/login')
    user = authenticate(email=email, password=password)
    if user is not None:
        auth_login(request, user)
        message = '登录成功'
        return redirect('/home/files')
    else:
        message = '用户名或密码不正确'
        return render(request,'accounts/login.html',locals())

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")

def  forget_password(request):
    email = request.GET['email']
