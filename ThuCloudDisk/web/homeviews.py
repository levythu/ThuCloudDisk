# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from web.models import MyUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from ThuCloudDisk import settings
if settings.USE_SWIFT:
    from web.swift import *
import os
import json
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@login_required(login_url='/login')
@csrf_protect
def files(request):
    user = request.user
    file_list = []

    if request.GET.has_key('current_dir'):
        current_dir= request.GET['current_dir']
    else:
        current_dir= ''

    if settings.USE_SWIFT:
        swift = Swift()
        swift.connect()
        tuple =  swift.list_container(user.email);
        if tuple == None:
            swift.put_container(user.email)
            tuple = swift.list_container(user.email)

        for f in tuple[1]:
            this_dir = './'
            fileType = 'file'
            file_list.append({'this_dir':this_dir,'filetype':fileType,'name':f['name'],'last_modified':f['last_modified'],'bytes':f['bytes']})

    else:
        user_path = os.path.join(settings.LOCAL_BUFFER_PATH,request.user.email,current_dir)
        file_list=[]
        files =  os.listdir(user_path)
        for f in files:

            #print datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(user_path,f)))
            abs_path = os.path.join(user_path,f)
            abs_path = abs_path.encode('utf-8')
            fileType = 'file'
            this_dir = './'
            if os.path.isdir(abs_path):
                fileType = 'folder'
                this_dir = os.path.join(current_dir,f)
                this_dir = this_dir.encode('utf-8')
            file_list.append({'this_dir':this_dir,'filetype':fileType,'name':f,'bytes':os.path.getsize(abs_path),'last_modified':datetime.datetime.fromtimestamp(os.path.getmtime(abs_path))})

    sort_method = 'asc'
    if not request.GET.has_key('order_by'):
        file_list = sorted(file_list,key = lambda k:k['last_modified'],reverse=True)

    else:
        order_by = request.GET['order_by']
        if order_by == 'filename':
            file_list = sorted(file_list,key = lambda k:k['name'])
        elif order_by == 'size':
            file_list = sorted(file_list,key = lambda k:k['bytes'])
        else:
            file_list = sorted(file_list,key = lambda k:k['last_modified'],reverse=True)
        if request.GET.has_key('sort_method'):
            sort_method = request.GET['sort_method']
            if sort_method == 'desc':
                file_list = reversed(file_list)
            sort = 'desc'
    filelevel_list = current_dir.split('/')
    if '' in filelevel_list:
        filelevel_list.remove('')
    final_filelevel_list = []
    levelname = {}
    if filelevel_list.__len__() > 0:
        current_level = ''
        for level in filelevel_list:
            current_level += level + '/'
            final_filelevel_list.append({'href':current_level,'name':level})

    return render(request,'home/files.html',locals())
