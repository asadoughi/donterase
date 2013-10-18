from django.conf.urls import patterns, url

from files import views

urlpatterns = patterns('',
                       url(r'^get$', views.get, name='get'),
                       url(r'^latest$', views.latest, name='latest'),
                       url(r'^submit*$', views.submit, name='submit'),
                       url(r'^tags*$', views.tags, name='tags'),
                       url(r'^upload*$', views.upload, name='upload'),
                       )
