# This Python file uses the following encoding: utf-8
from django import forms
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from web.models import MyUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required 

@login_required(login_url='/login')
def home(request):
    user = request.user
    return render_to_response('home/home.html',locals())