from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^files/', include('files.urls')),
                       )
