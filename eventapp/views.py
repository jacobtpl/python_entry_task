import random
import hashlib
import json
import jwt

from django.http import HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.test import RequestFactory

from dateutil.parser import parse

from eventapp import USERNAMES, PASSWORDS

from .models import Event
from .models import User
from .models import Like
from .models import Participation
from .models import Comment

MAX_PAGE_SIZE = 20

#util functions *************************

def serialize_user(qset):
	raw_data = serializers.serialize('python', qset, fields=('name', 'username'))
	actual_data = [{**{'user_id': d['pk']}, **d['fields']} for d in raw_data]
	output = json.dumps(actual_data, cls=DjangoJSONEncoder)
	return output

def serialize_event(qset):
	output_data = []
	for e in qset.all():
		d = model_to_dict(e)
		image_set = e.image_set.values()
		like_set = e.like_set.values()
		part_set = e.participation_set.values()
		comment_set = e.comment_set.order_by('-created').values()
		output_data.append({**d, **{'created': e.created, 'updated': e.updated}, **{'images': [l['image_path'] for l in image_set]},
			**{'likes': [l['user_id'] for l in like_set]}, **{'participants': [p['user_id'] for p in part_set]}, **{'comments': [c['comment_id'] for c in comment_set]}})
	output = json.dumps(output_data, cls=DjangoJSONEncoder)
	return output

def serialize_comment(qset):
	raw_data = serializers.serialize('python', qset)
	actual_data = [{**{'comment_id': d['pk']}, **d['fields']} for d in raw_data]
	output = json.dumps(actual_data, cls=DjangoJSONEncoder)
	return output

def serialize_like(qset):
	raw_data = serializers.serialize('python', qset)
	actual_data = [{**{'like_id': d['pk']}, **d['fields']} for d in raw_data]
	output = json.dumps(actual_data, cls=DjangoJSONEncoder)
	return output

def serialize_participate(qset):
	raw_data = serializers.serialize('python', qset)
	actual_data = [{**{'participation_id': d['pk']}, **d['fields']} for d in raw_data]
	output = json.dumps(actual_data, cls=DjangoJSONEncoder)
	return output

def authenticate(request):
	token = request.META.get('HTTP_TOKEN', '')
	if token == '':
		return None

	try:
		obj = jwt.decode(token, verify=False)
	except jwt.exceptions.DecodeError:
		return None

	username = obj.get('username', '')
	if username == '':
		return None

	try:
		u = User.objects.get(username=username)
	except User.DoesNotExist:
		return None

	try:
		jwt.decode(token, u.salt, algorithms=['HS256'])
	except jwt.exceptions.InvalidSignatureError:
		return None

	return u
#end util functions *************************


#POST to /sessions/
def login(request):
	username = request.POST.get('username', '')
	if username == '':
		return HttpResponse(content='User does not exist.', status=401)
	password = request.POST.get('password', '')

	us = User.objects.filter(username=username).values('username', 'passhash', 'salt')
	if len(us) == 1:
		u = us[0]
	else:
		return HttpResponse(content='User does not exist.', status=401)

	computedhash = hashlib.sha256(str.encode(password+u['salt'])).hexdigest()
	if computedhash == u['passhash']:
		encoded_jwt = jwt.encode({'username': username}, u['salt'], algorithm='HS256')
		return HttpResponse(content='{"jwt":"'+encoded_jwt.decode("utf-8")+'"}')
	else:
		return HttpResponse(content='Incorrect password.', status=200)

#GET to /testlogin/
def testlogin(request):
	i = random.randint(0, 999999)
	nr = RequestFactory().post('/sessions/', {'username': USERNAMES[i], 'password': PASSWORDS[i]})
	return login(nr)

#GET to /events/
def showevents(request):
	if request.method == 'GET':
		user = authenticate(request)
		if user is None:
			return HttpResponse(content='Invalid authorization.', status=401)

		filter_tag = request.GET.get('tag', '')
		filter_start = request.GET.get('start', '')
		filter_end = request.GET.get('end', '')

		cur_query_set = Event.objects.all()
		if filter_tag != '':
			cur_query_set = cur_query_set.filter(tags__contains=filter_tag)
		if filter_start != '':
			fstart = parse(filter_start)
			cur_query_set = cur_query_set.filter(start__gte=fstart)
		if filter_end != '':
			fend = parse(filter_end)
			cur_query_set = cur_query_set.filter(end__lte=fend)

		offset = int(request.GET.get('offset', '0'))
		page_size = int(request.GET.get('page_size', '20'))
		if page_size > MAX_PAGE_SIZE:
			return HttpResponse(content='Page size too large.', status=400)

		output = serialize_event(cur_query_set.order_by('-start')[offset:(offset+page_size)])
		return HttpResponse(output)

	elif request.method == 'POST':
		user = authenticate(request)
		if user is None or not user.admin:
			return HttpResponse(content='Invalid authorization.', status=401)
		name = request.POST.get('name', '')
		desc = request.POST.get('description', '')
		tags = request.POST.get('tags', '')
		start = request.POST.get('start', '')
		st = parse(start)
		end = request.POST.get('end', '')
		et = parse(end)
		e = Event(name=name, description=desc, tags=tags, start=st, end=et, created=timezone.now(), updated=timezone.now())
		e.save()
		return HttpResponse(status=200)
	else:
		return None

#GET to /events/<ID>/
def eventdetail(request, qid):
	user = authenticate(request)
	if user is None:
		return HttpResponse(content='Invalid authorization.', status=401)

	output = serialize_event(Event.objects.filter(event_id=qid))
	return HttpResponse(output[1:-1])

#GET to /users/<ID>/
def userdetail(request, qid):
	user = authenticate(request)
	if user is None:
		return HttpResponse(content='Invalid authorization.', status=401)
	output = serialize_user(User.objects.filter(user_id=qid))
	return HttpResponse(output[1:-1])

#GET to /events/likes/
def viewlike(request, qid):
	user = authenticate(request)
	if user is None:
		return HttpResponse(content='Invalid authorization.', status=401)

	output = serialize_like(Like.objects.filter(like_id=qid))
	return HttpResponse(output[1:-1])

#POST to /events/likes/
def setlike(request):
	user = authenticate(request)
	if user is None:
		return HttpResponse(content='Invalid authorization.', status=401)

	event_id = int(request.POST.get('event_id', '-1'))
	if event_id == -1:
		return HttpResponse(content='Invalid event.', status=401)

	try:
		e = Event.objects.get(event_id=event_id)
	except Event.DoesNotExist:
		return HttpResponse(content='Invalid event.', status=401)

	like_val = request.POST.get('like', '')
	if like_val == '':
		return HttpResponse(content='Please provide like value.', status=400)

	changed = False
	if int(like_val) == 0:
		if Like.objects.filter(event_id=e, user_id=user).exists():
			changed = True
			l = Like.objects.get(event_id=e, user_id=user)
			l.delete()
	else:
		if Like.objects.filter(event_id=e, user_id=user).exists() is False:
			changed = True
			l = Like(event_id=e, user_id=user)
			l.save()

	return HttpResponse(str(changed))

#GET to /events/participations/
def viewparticipate(request, qid):
	user = authenticate(request)
	if user is None:
		return HttpResponse(content='Invalid authorization.', status=401)

	output = serialize_participate(Participation.objects.filter(participation_id=qid))
	return HttpResponse(output[1:-1])

#POST to /events/participations/
def setparticipate(request):
	user = authenticate(request)
	if user is None:
		return HttpResponse(content='Invalid authorization.', status=401)

	event_id = int(request.POST.get('event_id', '-1'))
	if event_id == -1:
		return HttpResponse(content='Invalid event.', status=401)

	try:
		e = Event.objects.get(event_id=event_id)
	except Event.DoesNotExist:
		return HttpResponse(content='Invalid event.', status=401)

	participate_val = request.POST.get('participate', '')
	if participate_val == '':
		return HttpResponse(content='Please provide participate value.', status=400)

	changed = False
	if int(participate_val) == 0:
		if Participation.objects.filter(event_id=e, user_id=user).exists():
			changed = True
			p = Participation.objects.get(event_id=e, user_id=user)
			p.delete()
	else:
		if Participation.objects.filter(event_id=e, user_id=user).exists() is False:
			changed = True
			p = Participation(event_id=e.event_id, user_id=user.user_id)
			p.save()

	return HttpResponse(str(changed))

#GET to /comments/<ID>/
def viewcomment(request, qid):
	user = authenticate(request)
	if user is None:
		return HttpResponse(content='Invalid authorization.', status=401)
	output = serialize_comment(Comment.objects.filter(comment_id=qid))
	return HttpResponse(output[1:-1])

#POST to /comments/
def postcomment(request):
	user = authenticate(request)
	if user is None:
		return HttpResponse(content='Invalid authorization.', status=401)

	event_id = int(request.POST.get('event_id', '-1'))
	if event_id == -1:
		return HttpResponse(content='Invalid event.', status=401)

	if Event.objects.filter(event_id=event_id).exists() is False:
		return HttpResponse(content='Invalid event.', status=401)

	text = request.POST.get('text', '')
	if text == '':
		return HttpResponse(content='Comment is empty.', status=400)

	c = Comment(event_id=event_id, user_id=user.user_id, text=text)
	c.save()

	return HttpResponse(status=200)
