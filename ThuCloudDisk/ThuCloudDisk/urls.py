from django.conf.urls import patterns, include, url

from django.contrib.auth.views import password_reset,password_reset_done,password_reset_confirm,password_reset_complete
from web.accountviews import *
from web.homeviews import *
#from web.authviews import *
from web.permissionviews import *
from web.filehandler import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', login),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':'media/'}),
    url(r'^home/files',files),
    url(r'^login$',login),
    url(r'^login_do$',login_do),
    url(r'^register$',register),
    url(r'^register_do$',register_do),
    url(r'^password_reset$',password_reset,{'template_name':'accounts/password_reset_form.html',\
                            'email_template_name':'accounts/password_reset_email.html',\
                            'post_reset_redirect':'/password_reset_done',\
                            }),
    url(r'^password_reset_done$',password_reset_done,{'template_name':'accounts/password_reset_done.html'}),
    url(r'^password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',password_reset_confirm,\
                            {'template_name': 'accounts/password_reset_confirm.html','post_reset_redirect':'/password_done'}),
    url(r'^password_done$',password_reset_complete,{'template_name':'accounts/password_reset_complete.html'}),
    url(r'^logout$',logout),
    url(r'^uploadhandler$',uploadhandler),
    url(r'^download_file',download_file),
    url(r'^delete_file',delete_file),
    url(r'^rename_file',rename_file),
    url(r'^batchDownload',batch_download),
    # Examples:
    # url(r'^$', 'ThuCloudDisk.views.home', name='home'),
    # url(r'^ThuCloudDisk/', include('ThuCloudDisk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
