from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.showevents, name='showevents'),
	url(r'^likes/$', views.setlike, name='setlike'),
	url(r'^participations/$', views.setparticipate, name='setparticipate'),
	url(r'^likes/(?P<qid>[0-9]+)/$', views.viewlike, name='viewlike'),
	url(r'^participations/(?P<qid>[0-9]+)/$', views.viewparticipate, name='viewparticipate'),
	url(r'^(?P<qid>[0-9]+)/$', views.eventdetail, name='eventdetail')
]
