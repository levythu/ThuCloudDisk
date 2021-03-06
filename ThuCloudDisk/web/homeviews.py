# -*- coding: utf-8 -*-
import mimetypes
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
from web.utilities import sanitize, setClear
if settings.USE_SWIFT:
    from web.swift import *
import os
import json
import datetime
import sys
reload(sys)
import time
import re
sys.setdefaultencoding('utf-8')

@login_required(login_url='/login')
@csrf_protect
def files(request):
    user = request.user
    file_list = []
    WEB_RSYNC = settings.WEB_RSYNC
    if request.GET.has_key('current_dir'):
        current_dir= request.GET['current_dir']
    else:
        current_dir= ''
    current_dir=setClear(sanitize(current_dir))

    if request.GET.has_key('order_by'):
        order_by = request.GET['order_by']
    if request.GET.has_key('sort_method'):
        sort_method = request.GET['sort_method']

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

    lc=locals()
    return render(request,'home/files.html', lc)
    #return render(request,'basic-plus.html')
def filelist(request):
    RenameAllowed = False
    user = request.user
    file_list = []
    WEB_RSYNC = settings.WEB_RSYNC
    if request.GET.has_key('current_dir'):
        current_dir= request.GET['current_dir']
    else:
        current_dir= ''
    current_dir=setClear(sanitize(current_dir))

    if settings.USE_SWIFT:
        swift = Swift()
        swift.connect()
        prefix = current_dir
        if prefix == '':
            prefix = None
        else:
            prefix = prefix

        tuple =  swift.list_container(user.email,prefix=prefix,delimiter='/');
        if tuple == None:
            swift.put_container(user.email)
            tuple = swift.list_container(user.email,prefix=prefix,delimiter='/')

        for f in tuple[1]:
            if f.has_key('bytes'):

                fname = f['name'].split('/')[-1]
                fname = fname.replace('/','')
                if fname == '':
                    continue

                this_dir = './'
                fileType = 'file'
                filesize = int(f['bytes'])
                if(filesize < 1000):
                    filesize = filesize.__str__() +' B'
                elif(filesize < 1000*1000):
                    filesize = (int(float(filesize)/1000)).__str__() +' KB'
                elif(filesize < 1000*1000*1000):
                    filesize = (round(float(filesize)/1000/1000,1)).__str__() +' MB'
                last_modified = f['last_modified']
                pattern = re.compile(r'\.\d{6}',re.S)
                last_modified = pattern.sub('',last_modified)
                last_modified = last_modified.replace('T',' ')
                icon = 'text-icon icon'

            else:
                icon = 'folder-icon icon'
                this_dir = f['subdir']
                fname = f['subdir']
                fname = fname.split('/')
                fname = fname[-2]
                last_modified = ''
                filesize = 0
                fileType = 'dir'

            file_list.append({'icon':icon,'this_dir':this_dir,'filetype':fileType,'name':fname,'last_modified':last_modified,'bytes':filesize})

    else:
        user_path = os.path.join(settings.LOCAL_BUFFER_PATH,request.user.email,current_dir)
        file_list=[]
        files =  os.listdir(user_path)
        for f in files:

            #print datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(user_path,f)))
            abs_path = os.path.join(user_path,f)
            abs_path = abs_path.encode('utf-8')
            type,encoding = mimetypes.guess_type(abs_path)
            if type == None:
                icon='glyphicon glyphicon-file icon'
            elif type.split('/')[0] == 'image':
                icon = 'image-icon icon'
            elif type == 'application/zip':
                icon = 'zip-icon icon'
            elif type == 'application/pdf':
                icon= 'pdf-icon icon'
            elif type.split('/')[0] == 'video':
                icon = 'icon video-icon'
            elif type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or type=='application/msword':
                icon = 'word-icon icon'
            elif type=='application/vnd.ms-xpsdocument':
                icon = 'xps-icon icon'
            elif type.split('/')[0] == 'text':
                icon = 'text-icon icon'
            elif type == 'application/vnd.ms-excel' or type =='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                icon = 'excel-icon icon'
            elif type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation' or type == 'application/mspowerpoint':
                icon = 'ppt-icon icon'
            else:
                icon='glyphicon glyphicon-file icon'

            this_dir = './'
            fileType = 'file'
            if os.path.isdir(abs_path):
                icon = 'folder-icon icon'
                fileType = 'dir'
                this_dir = os.path.join(current_dir,f)
                this_dir = this_dir.encode('utf-8')

            rawsize = os.path.getsize(abs_path)
            filesize = rawsize
            if(filesize < 1000):
                filesize = filesize.__str__() +' B'
            elif(filesize < 1000*1000):
                filesize = (int(float(filesize)/1000)).__str__() +' KB'
            elif(filesize < 1000*1000*1000):
                filesize = (round(float(filesize)/1000/1000,1)).__str__() +' MB'
            last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(abs_path));

            last_modified_format = datetime.datetime(last_modified.year, last_modified.month, last_modified.day, last_modified.hour, last_modified.minute, last_modified.second)
            last_modified_str =  last_modified_format.__str__()

            file_list.append({'this_dir':this_dir,'filetype':fileType,'icon':icon,'name':f,'rawsize':rawsize,'bytes':filesize,'last_modified':last_modified_str})

    sort_method = 'asc'
    if not request.GET.has_key('order_by'):
        file_list = sorted(file_list,key = lambda k:k['last_modified'],reverse=True)

    else:
        order_by = request.GET['order_by']
        if order_by == 'filename':
            file_list = sorted(file_list,key = lambda k:k['name'])
        elif order_by == 'size':
            file_list = sorted(file_list,key = lambda k:k['rawsize'])
        else:
            file_list = sorted(file_list,key = lambda k:k['last_modified'],reverse=True)
        if request.GET.has_key('sort_method'):
            sort_method = request.GET['sort_method']
            if sort_method == 'desc':
                file_list = reversed(file_list)
            sort = 'desc'
    lc=locals()
    return render(request,'home/fileList.html', lc)
