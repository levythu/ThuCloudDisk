# This Python file uses the following encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from web.models import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from ThuCloudDisk import  settings
from django.core.servers.basehttp import FileWrapper
if settings.USE_SWIFT:
    from web.swift import *
import os
import magic
from ThuCloudDisk import settings
import json
import datetime
def file_extension(path):
    return os.path.splitext(path)[1]
def get_timestamp():
    t = datetime.datetime.now()
    t = t.__str__()
    t = t.replace(' ','')
    t = t.replace('-','')
    t = t.replace(':','')
    t = t.replace('.','')
    return t
def handle_uploaded_file(email,f):

    root_path = settings.LOCAL_BUFFER_PATH
    file_path = os.path.join(root_path,email,str(f))

    if os.path.exists(file_path):
        basename = os.path.splitext(file_path)[0]
        basename = basename + '_'+ get_timestamp()
        file_path = basename + file_extension(file_path)
    with open(file_path,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if settings.USE_SWIFT:
        swift = Swift()
        swift.connect()
        swift.put_object_from_file(container = email,prefix = '',filepath = file_path)
    return HttpResponseRedirect('/home/files')
@csrf_protect
def uploadhandler(request):

    file = request.FILES['file']
    handle_uploaded_file(request.user.email,file)

    return HttpResponseRedirect('/home/files')

import urllib
import mimetypes
def download_file(request):
    email = request.user.email
    file_name = request.GET['file_name']
    file_path = os.path.join(settings.LOCAL_BUFFER_PATH,email,file_name)
    if not os.path.exists(file_path):
        if settings.USE_SWIFT:
            swift = Swift()
            swift.connect()
            swift.get_object_to_file(email,file_name)
    type,encoding = mimetypes.guess_type(file_path)
    if type is None:
        content_type = magic.from_file(file_path,mime=True)
        if content_type == 'application/msword':
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        content_type = type
    f = open(file_path)
    response = HttpResponse(FileWrapper(f),content_type=content_type)
    response['Content-encoding'] = encoding
    response['Content-Length'] = os.path.getsize(file_path) 

    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        filename_header = 'filename=%s' % file_name.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        filename_header = ''
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(file_name.encode('utf-8'))

    else:
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(file_name.encode('utf-8'))
    response['Content-Disposition'] = 'attachement; '+ filename_header
    return response
@csrf_protect
def delete_file(request):
    file_name = request.POST['file_name']
    if settings.USE_SWIFT:
        swift = Swift()
        swift.connect()
        swift.delete_object(request.user.email,file_name)
    try:
        buffer_path  = os.path.join(settings.LOCAL_BUFFER_PATH,request.user.email,file_name)
        os.remove(buffer_path)
    except:
        print 'fail to delete'+file_name
    return HttpResponseRedirect('/home/files')

@csrf_protect
def rename_file(request):
    old_name = request.GET['old_name']
    new_name = request.GET['new_name']
    #todo swfit rename
    try:
        buffer_path = os.path.join(settings.LOCAL_BUFFER_PATH,request.user.email,old_name)
        new_path = os.path.join(settings.LOCAL_BUFFER_PATH,request.user.email,new_name)
        print buffer_path
        print new_path
        os.renames(buffer_path,new_path)
    except:
        print 'fail to rename'+old_name
    return HttpResponseRedirect('/home/files')
