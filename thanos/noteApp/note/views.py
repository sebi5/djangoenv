# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
import requests
from random import randint
from django.core.validators import validate_email
from django.http import HttpResponse
import sqlite3 as sql

from note.models import Userdata

# home/index page
def home(request):
	return render(request, 'index.html')
		
# auth page
def auth(request):
	if request.method == 'GET':
		rows = Userdata.objects.all()
		data = {"alarms":rows}
		return render(request, 'auth.html', data)

	if request.method == 'POST' and request.POST.get('todo') != None:
		todo = request.POST.get('todo')
		todo = todo.upper()
		rand_id = str(randint(10000, 99999)) + str(randint(10000, 99999)) + str(randint(10000, 99999))
		p = Userdata(user_id=rand_id, content=todo)
		p.save()
		post_url = "https://bellbird.joinhandshake-internal.com/push"
		r = requests.post(post_url, json = {"alarm_id":rand_id, "todo":todo})
		print(r.text)
		if r.status_code == 200:
			return redirect('auth')
			
		
		
		
	


		