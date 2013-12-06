from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

from sblog.core.views import *

urlpatterns = patterns('',
    url(r'^$', BlogView.as_view(), name='blog'),
    url(r'^post/(?P<pk>\d+)/$', PostView.as_view(), name='post'),
    url(r'^edit_post/(?P<pk>\d+)/$', EditPostView.as_view(), name='edit_post'),
    url(r'^create_post/$', CreatePostView.as_view(), name='create_post'),
    url(r'^delete_post/(?P<pk>\d+)/$', DeletePostView.as_view(), name='delete_post'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)