# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-05 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('eventapp', '0001_initial'),
	]

	operations = [
		migrations.AlterField(
			model_name='user',
			name='username',
			field=models.CharField(max_length=64),
		),
	]