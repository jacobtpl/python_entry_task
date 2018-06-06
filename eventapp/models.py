from django.db import models

# Create your models here.
class User(models.Model):
	user_id = models.AutoField(primary_key=True)

	name = models.CharField(max_length=200)
	username = models.CharField(max_length=64, db_index=True)
	passhash = models.CharField(max_length=70)
	salt = models.CharField(max_length=32)
	admin = models.BooleanField()

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "user_tab"

	def __str__(self):
		return self.username


class Event(models.Model):
	event_id = models.AutoField(primary_key=True)

	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	tags = models.CharField(max_length=200)

	start = models.DateTimeField()
	end = models.DateTimeField()

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "event_tab"

	def __str__(self):
		return self.name

class Like(models.Model):
	like_id = models.AutoField(primary_key=True)

	user = models.ForeignKey('User', on_delete=models.CASCADE)
	event = models.ForeignKey('Event', on_delete=models.CASCADE)

	class Meta:
		db_table = "like_tab"

class Participation(models.Model):
	participation_id = models.AutoField(primary_key=True)

	user = models.ForeignKey('User', on_delete=models.CASCADE)
	event = models.ForeignKey('Event', on_delete=models.CASCADE)

	class Meta:
		db_table = "participation_tab"

class Image(models.Model):
	image_id = models.AutoField(primary_key=True)

	image_path = models.CharField(max_length=400)
	event = models.ForeignKey('Event', on_delete=models.CASCADE)

	class Meta:
		db_table = "image_tab"

class Comment(models.Model):
	comment_id = models.AutoField(primary_key=True)

	user = models.ForeignKey('User', on_delete=models.CASCADE)
	event = models.ForeignKey('Event', on_delete=models.CASCADE)

	text = models.CharField(max_length=500)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "comment_tab"
