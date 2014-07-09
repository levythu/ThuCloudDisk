#-*-coding:utf-8-*-
import os
import sys

app_path='/home/thucloud2/ThuCloudDisk'
sys.path.append(app_path)
#os.chdir(app_path)
os.environ['DJANGO_SETTINGS_MOULE']='ThuCloudDisk.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE","ThuCloudDisk.settings")
import django.core.handlers.wsgi
application=django.core.handlers.wsgi.WSGIHandler()

