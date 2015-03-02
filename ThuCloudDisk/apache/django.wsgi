#-*-coding:utf-8-*-
import os
import sys

app_path='/home/thucloud1/ThuCloudDisk/ThuCloudDisk'
sys.path.append(app_path)
os.chdir(app_path)
os.environ['DJANGO_SETTINGS_MOULE']='ThuCloudDisk.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE","ThuCloudDisk.settings")
import django.core.wsgi
application=django.core.wsgi.get_wsgi_application()

