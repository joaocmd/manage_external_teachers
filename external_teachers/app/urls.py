# App urls
# Mapping between urls and views

from django.conf.urls import patterns, include, url

from app import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^about/', views.about, name='about'),
		url(r'^logout/', views.user_logout, name='logout'),
		url(r'^sc/', views.sc, name='sc'),
		url(r'^dep', views.dep, name='dep'),
)
