from django.conf.urls import patterns, include, url
from BlogApp.views import *
from django.views.decorators.csrf import csrf_exempt
from BlogApp.rest_views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Blog.views.home', name='home'),
    # url(r'^Blog/', include('Blog.foo.urls')),
    url(r'^myblog/$', show_home),
    url(r'^editblog/(?P<id>\d+)/$', edit_blog),
    url(r'^myblog/(?P<id>\w+)/$', show_blog),
    url(r'^addblog/$', add_blog),
    url(r'^deleteblog/(?P<id>\d+)/$', delete_blog),
    url(r'^resetstats/$', reset_stats),
    url(r'^createuser/$', create_user),
    url(r'^login/$', auth),
    url(r'^logout/$', leave),

    # REST api
    url(r'^api/v1/blogs/$', blogs),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)
