from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.postcomment, name='postcomment'),
	url(r'^(?P<qid>[0-9]+)/$', views.viewcomment, name='viewcomment')
]
