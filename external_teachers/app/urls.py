# App urls
# Mapping between urls and views

from django.conf.urls import patterns, include, url

from app import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^about/', views.about, name='about'),
		url(r'^logout/', views.user_logout, name='logout'),
		url(r'^sc_opened/', views.sc_opened, name='sc_opened'),
		url(r'^sc_closed', views.sc_closed, name='sc_closed'),
		url(r'^dep_opened/', views.dep_opened, name='dep_opened'),
		url(r'^dep_closed/', views.dep_closed, name='dep_closed'),
		url(r'^dep_prop_new/', views.dep_prop_new, name='dep_prop_new'),
		url(r'^name/', views.name, name='name'),
		url(r'^edit/(?P<pk>\d+)/$', views.edit, name='edit'),
		url(r'^park/(?P<pk>\d+)/$', views.change_park, name='change_park'),
		url(r'^card/(?P<pk>\d+)/$', views.change_card, name='change_card'),
		url(r'^pro_cat/(?P<pk>\d+)/$', views.change_professional_category, name='change_pro_cat'),
		url(r'^externalteachers/(?P<pk>\d+)/$', views.get_external_teacher, name='get_external_teacher'),
)
