# This Python file uses the following encoding: utf-8
from django import forms
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from web.models import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import time
import hashlib
import re
import json
from xml.dom import minidom

from web.oss.oss_api import *
from web.oss.oss_xml_handler import *
HOST="oss.aliyuncs.com"
ACCESS_ID = "eNHTL5wHM8z4iPah"
SECRET_ACCESS_KEY = "wNJUSWBJPdQOWYHVMBA2eqx5Uhnswd"
TIMEOUT = 600
oss = OssAPI(HOST,ACCESS_ID,SECRET_ACCESS_KEY)

def sign_url(request):
    user_email = request.user.email
    method='GET'
    bucket=request.GET['bucket']
    object=request.GET['object']
    headers = {}
    headers['Content-MD5'] = request.GET['Content_MD5']
    headers['Content-Type'] = request.GET['Content_Type']
    userPermission = user_has_permisson_to_object(request.user.email,bucket,object)
    if(userPermission == 'noPermission'):
        return HttpResponse(json.dumps({'permission':userPermission}))
    url = "http://"+ bucket + "." + HOST  + "/"+object
    resource = "/" + bucket + "/" + object
    url_with_auth = oss.sign_url_auth_with_expire_time(method, url, headers, resource, TIMEOUT)
    return HttpResponse(json.dumps({'permission':userPermission,'url_with_auth':url_with_auth}))
#build a bucket for the user when a new user register   
#todo better：to prevent the conflict bucket name, re generate a new bucket name after 1s
def build_bucket(user):
    user_email = user.email
    try:
        local_bucket =  userBucket.objects.get(ownerMail = user_email)
    except Exception as err:
        acl = 'private'
        headers = {}
        new_bucket = user.id + '--'+ time.strftime("%Y-%b-%d%H-%M-%S").lower()
        hashed_bucket = hashlib.new("md5",new_bucket).hexdigest()
        res = oss.put_bucket(hashed_bucket, acl, headers)
        if (res.status / 100) == 2:
            local_bucket = userBucket(ownerMail=user_email,bucket=new_bucket)
            local_bucket.save()
        else:
            print "put bucket ", bucket, "ERROR"
            time.spleep(1)
            build_bucket(user) 
            return False
    return True
#get the user bucket for the user
def get_bucket_name(email):
    try:
        bucket =  userBucket.objects.get(ownerMail = email)
        return bucket.bucket
    except Exception as err:
        return False
    

def belong_to(childObject,parentObject):
    pattern = re.compile(r'^'+parentObject);
    if(pattern.match(childObject)):
        return True
    return False

#whether user has permission to access to the object
def user_has_permisson_to_object(user_email,bucket,object):
    try:
        user_bucket = userBucket.objects.get(ownerMail=user_email)
        if(belong_to(bucket,user_bucket.bucket)):
            return 'ownObject'
        else:
            #other users share to this user
            sharedObjectList = shareObject.objects.filter(sharerMail = user_email)
            for sharedObject in sharedObjectList:
                if(belong_to('/'+bucket+'/'+object,sharedObject.object)):
                    return 'sharedObject'
            publicBucketList = publicObject.objects.all()
            for public_object in publicBucketList:
                if(belong_to('/'+bucket+'/'+object,public_object.object)):
                    return 'publicObject'
    except Exception as err:
        print(err)
    return 'noPermission'
#list a user's bucket
def list_bucket(request):
    user_email = request.user.email
    bucket = get_bucket_name(user_email)
    if(bucket):
        object=''
        marker = ''
        delimiter = '/'
        res = oss.get_bucket(bucket,object,marker,delimiter)
        if (res.status / 100) == 2:
            xml_string = res.read()
            xml = minidom.parseString(xml_string)
            bucket_name = get_tag_text(xml,'Name')
            prefix = get_tag_text(xml,'Prefix')
            contents = xml.getElementsByTagName('Contents')
            content_list = []
            for c in contents:
                content_list.append(Content(c))
            object_list = []
            for c in content_list:
                url = "http://"+ bucket_name + "." + HOST  + "/" + c.key
                resource = "/" + bucket_name +"/" + c.key
                headers={}
                headers['Content-MD5'] = ''
                headers['Content-Type']=''
                url_with_auth = oss.sign_url_auth_with_expire_time('GET', url, headers, resource, TIMEOUT)
                object_list.append({'object_name':c.key,'last_modified':c.last_modified,'size':c.size,'bucket_name':bucket_name,'prefix':prefix,'url_with_auth':url_with_auth})
            CommonPrefixes = xml.getElementsByTagName('CommonPrefixes')
            if len(CommonPrefixes) > 0:
                folders = CommonPrefixes[0].getElementsByTagName('Prefix')
                for f in folders:
                    folder_name = f.childNodes[0].data
                    folder = oss.get_object(bucket,folder_name)
                    if (res.status / 100) == 2:
                        folder_headers = folder.getheaders()
                        folder_info = {}
                        for h in folder_headers:
                            folder_info[h[0]] = h[1]
                        object_list.append({'object_name':folder_name,'last_modified':folder_info['last-modified'],'size':0,'bucket_name':bucket_name,'prefix':'','url_with_auth':''})
            return HttpResponse(json.dumps(object_list))
    return HttpResponse(False)
def list_object(request):
    bucket = request.GET['bucket']
    object = request.GET['object']
    userPermission = user_has_permisson_to_object(request.user.email,bucket,object)
    if(userPermission=="noPermission"):
        return HttpResponse(json.dumps({'permission':userPermission}))
    marker = ''
    delimiter = '/'
    res = oss.get_bucket(bucket,object,marker,delimiter)
    if (res.status / 100) == 2:
        xml_string = res.read()
        xml = minidom.parseString(xml_string)
        bucket_name = get_tag_text(xml,'Name')
        prefix = get_tag_text(xml,'Prefix')
        contents = xml.getElementsByTagName('Contents')
        content_list = []
        for c in contents:
            content_list.append(Content(c))
        object_list = []
        for c in content_list:
            url = "http://"+ bucket_name + "." + HOST  + "/" + c.key
            resource = "/" + bucket_name +"/" + c.key
            headers={}
            headers['Content-MD5'] = ''
            headers['Content-Type']=''
            url_with_auth = oss.sign_url_auth_with_expire_time('GET', url, headers, resource, TIMEOUT)
            object_list.append({'object_name':c.key,'last_modified':c.last_modified,'size':c.size,'bucket_name':bucket_name,'prefix':prefix,'url_with_auth':url_with_auth})
        CommonPrefixes = xml.getElementsByTagName('CommonPrefixes')
        if len(CommonPrefixes) > 0:
            folders = CommonPrefixes[0].getElementsByTagName('Prefix')
            for f in folders:
                folder_name = f.childNodes[0].data
                folder = oss.get_object(bucket,folder_name)
                if (res.status / 100) == 2:
                    folder_headers = folder.getheaders()
                    folder_info = {}
                    for h in folder_headers:
                        folder_info[h[0]] = h[1]
                    object_list.append({'object_name':folder_name,'last_modified':folder_info['last-modified'],'size':0,'bucket_name':bucket_name,'prefix':'','url_with_auth':''})    
        return HttpResponse(json.dumps(object_list))    
    return HttpResponse(False)
def download_file(request):
    bucket = request.GET['request']
    object = request.GET['object']
    filename = request.GET['filename']
    headers = {}
    res = oss.get_object_to_file(bucket, object, filename, headers)
    if (res.status / 100) == 2:
        print "get_object_to_file OK"
    else:
        print "get_object_to_file ERROR"