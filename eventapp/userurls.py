from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<qid>[0-9]+)/$', views.userdetail, name='userdetail')
]
