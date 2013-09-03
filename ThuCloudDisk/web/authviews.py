# This Python file uses the following encoding: utf-8
from django import forms
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from web.models import MyUser
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import json
import base64
import hmac
import sha
#get the home bucket for the user
def get_home_bucket(request):
    user = request.user
    print user_email
    access_key = {'access_key_id':'eNHTL5wHM8z4iPah','access_key_secret':'wNJUSWBJPdQOWYHVMBA2eqx5Uhnswd','host':'xiaohebucket.oss.aliyuncs.com'}
    access_key = json.dumps(access_key)
    return HttpResponse(access_key)
    
#get authorization header include access_key_id and signature    
@login_required(login_url='/login')
def get_authorization_header(request,bucket,object=None):
    access_key = get_access_key_secret(access_key_id)
    
#whether user is authenticated to access to the object
def is_user_authed_to_object(user_id,bucket,object=None):
    return True;
    
#private function
#get the access_key_id and access_key_secret by the bucket name
def get_access_key_secret(bucket):
    access_key = {id:'eNHTL5wHM8z4iPah','secret':'wNJUSWBJPdQOWYHVMBA2eqx5Uhnswd'}
    return access_key