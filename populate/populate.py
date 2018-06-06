from eventapp.models import Event
from eventapp.models import User
from eventapp.models import Comment
from eventapp.models import Participation
from eventapp.models import Image
from eventapp.models import Like

import random
import hashlib
import time
import io

from django.utils import timezone
from datetime import datetime
from datetime import timedelta

def clearAll():
	Event.objects.all().delete()
	User.objects.all().delete()
	Comment.objects.all().delete()
	Participation.objects.all().delete()
	Image.objects.all().delete()
	Like.objects.all().delete()


def createEvents(SIZE=1000000):
	print('Creating events:')
	random.seed()
	DELTA = 10000000

	curtime = round(time.time())

	words = []
	with io.open("words.txt", "r") as f:
	    words = f.read().split()

	tags = []
	with io.open("tags.txt", "r") as f:
	    tags = f.read().splitlines()

	names = []
	with io.open("event_names.txt", "r") as f:
	    names = f.read().splitlines()

	desc = ''
	with io.open("description.txt", "r") as f:
	    desc = f.read()

	for i in range(0,SIZE):
		t1 = timezone.now()+timedelta(seconds=random.randint(-DELTA,DELTA))
		t2 = timezone.now()+timedelta(seconds=random.randint(-DELTA,DELTA))
		e = Event(name=random.choice(names), description=desc, tags=random.choice(tags), start=min(t1,t2), end=max(t1,t2))
		e.save()
		if i%100 == 0:
			print(i)

def generateSalt(len=16):
	ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	chars=[]
	for i in range(16):
		chars.append(random.choice(ALPHABET))
	return (''.join(chars))

def createUser(name,username,password,admin=False):
	random.seed()
	newsalt = generateSalt(len);
	hash_object = hashlib.sha256(str.encode(password+newsalt))
	passhash = hash_object.hexdigest()
	u = User(name=name,username=username,passhash=passhash,salt=newsalt,admin=admin)
	u.save()

def createUsers(SIZE=1000):
	print('Creating users:')
	createUser(name='Jacob Teo',username='teojpl',password='Garena.com',admin=True)
	names = []
	with io.open("people.txt", "r") as f:
	    names = f.read().splitlines()
	passwords = []
	with io.open("passwords.txt", "r") as f:
	    passwords = f.read().splitlines()

	for i in range(0,SIZE):
		n = random.choice(names)
		un = ''.join(c.lower() for c in n if not c.isspace())
		pw = random.choice(passwords)
		ad = bool(random.getrandbits(1))
		createUser(name=n,username=un,password=pw,admin=ad)
		if i%100 == 0:
			print(i)

def populate():
	clearAll()
	createUsers()
	createEvents()