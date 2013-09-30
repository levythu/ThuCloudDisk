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
import json
import base64
import hmac
import sha
import urllib

import re
SELF_DEFINE_HEADER_PREFIX = "x-oss-"
def build_bucket(request):
    user_email = request.user.email
    try:
        bucket =  userBucket.objects.get(ownerMail = user_email)
    except Exception as err:
        bucket = userBucket(ownerMail=user_email,bucket='testbucket')
        bucket.save()
    return HttpResponse('yes')
#get the user bucket for the user
def get_bucket_name(request):
    user_email = request.user.email

    try:
        bucket =  userBucket.objects.get(ownerMail = user_email)
        return HttpResponse(bucket.bucket)
    except Exception as err:
        print(err)
        return HttpResponse('')
    
#return authorization header include access_key_id and signature   
def get_authorization_header(request):
    #bucket_name = request.POST['bucket_name'] # example-bucket
    object = request.GET['object']
    bucket = request.GET['bucket']
    method = request.GET['method']
    content_md5 = request.GET['content_md5']
    userPermission = user_has_permisson_to_object(request.user.email,bucket,object)
    if(userPermission == 'noPermission'):
        return HttpResponse(json.dumps({'permission':userPermission}))
    access_key = get_access_key_secret()
    
    sign_header = generate_signature(access_key,bucket,object,method,content_md5)
    header = json.dumps({'Expires':sign_header['Expires'],'Signature':sign_header['Signature'],'OSSAccessKeyId':sign_header['OSSAccessKeyId'],'permission':userPermission})
    return HttpResponse(header)
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
def generate_signature(access_key,bucket,object,method,content_md5):
    return sign_url_auth_with_expire_time(access_key,method,'/'+bucket+'/'+object)
    
#private function
#get the access_key_id and access_key_secret by the bucket name
def get_access_key_secret(bucket=None):
    access_key = {'id':'eNHTL5wHM8z4iPah','secret':'wNJUSWBJPdQOWYHVMBA2eqx5Uhnswd'}
    return access_key
def sign_url_auth_with_expire_time(access_key, method, resource="/", timeout=300, headers=None, params=None):
    '''
    Create the authorization for OSS based on the input method, url, body and headers
    :type method: string
    :param method: one of PUT, GET, DELETE, HEAD

    :type url: string
    :param:HTTP address of bucket or object, eg: http://HOST/bucket/object

    :type headers: dict
    :param: HTTP header

    :type resource: string
    :param:path of bucket or object, eg: /bucket/ or /bucket/object

    :type timeout: int
    :param

    Returns:
        signature url.
    '''
    if not headers:
        headers = {}
    if not params:
        params = {}
    send_time = str(int(time.time()) + timeout)
    headers['Date'] = send_time
    headers['Content-MD5'] = ''
    headers['Content-Type']=''
    auth_value = get_assign(access_key['secret'], method, headers, resource)
    params["OSSAccessKeyId"] = access_key['id']
    params["Expires"] = str(send_time)
    params["Signature"] = auth_value
    return params
def get_assign(secret_access_key, method, headers = None, resource="/", result = None):
    '''
    Create the authorization for OSS based on header input.
    You should put it into "Authorization" parameter of header.
    '''
    if not headers:
        headers = {}
    if not result:
        result = []
    content_md5 = ""
    content_type = ""
    date = ""
    canonicalized_oss_headers = ""
    content_md5 = headers['Content-MD5']
    content_type = headers['Content-Type']
    date = headers['Date']
    canonicalized_resource = resource
    print canonicalized_resource
    tmp_headers = _format_header(headers)
    if len(tmp_headers) > 0:
        x_header_list = tmp_headers.keys()
        x_header_list.sort()
        for k in x_header_list:
            if k.startswith(SELF_DEFINE_HEADER_PREFIX):
                canonicalized_oss_headers += k + ":" + tmp_headers[k] + "\n"
    string_to_sign = method + "\n" + content_md5.strip() + "\n" + content_type + "\n" + date + "\n" + canonicalized_oss_headers + canonicalized_resource;
    result.append(string_to_sign)
    h = hmac.new(secret_access_key, string_to_sign, sha)
    return base64.encodestring(h.digest()).strip()
########## function for Authorization ##########
def _format_header(headers = None):
    '''
    format the headers that self define
    convert the self define headers to lower.
    '''
    if not headers:
        headers = {}
    tmp_headers = {}
    for k in headers.keys():
        if isinstance(headers[k], unicode):
            headers[k] = headers[k].encode('utf-8')

        if k.lower().startswith(SELF_DEFINE_HEADER_PREFIX):
            k_lower = k.lower()
            tmp_headers[k_lower] = headers[k]
        else:
            tmp_headers[k] = headers[k]
    return tmp_headers