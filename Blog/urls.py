from django.conf.urls import patterns, include, url
from BlogApp.views import *

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

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)
