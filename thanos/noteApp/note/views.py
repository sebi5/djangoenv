# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
import requests
from random import randint
from django.core.validators import validate_email
from django.http import HttpResponse

from note.models import Userdata

# home/index page
def home(request):
	if request.session.has_key('session_email'):
		return redirect('profile')
	else:
		return render(request, 'index.html')
		
# auth page
def auth(request):
	if request.session.has_key('session_email'):
		return redirect('profile')
	else:
		if request.method == 'POST' and request.POST.get('code') == None:
			input_email = request.POST.get('email')
			try:
				input_email = input_email.lower()
			except:
				pass
			rand_code = randint(1000, 9999)
			rand_id = str(randint(10000, 99999)) + str(randint(10000, 99999)) + str(randint(10000, 99999))
			res_email = {'user_email':input_email} 
			
			try:
				email_is_valid = validate_email(input_email)
				email_passcode_url = "http://128.199.121.196/mailr/freemail.php?email=" + str(input_email) + "&code=" + str(rand_code)
				
				try:
					created = Userdata.objects.get(email=input_email)
					created = 1
				except:
					created = 0
					
				if created:
					Userdata.objects.select_for_update().filter(email=input_email).update(passcode=str(rand_code))
				else:
					if email_is_valid:
						p = Userdata(user_id=rand_id, email=input_email, content="", passcode=str(rand_code))
						p.save()
					else:
						err_msg = {'err':"Email is invalid", 'user_email':input_email}
						return render(request, 'auth.html', err_msg)
					
					
				r = requests.get(email_passcode_url)
				if r.status_code == 200:
					return render(request, 'auth.html', res_email)
				else:
					err_msg = {'err':"Please try again later.", 'user_email':input_email}
					return render(request, 'auth.html', err_msg)
			except:
				return redirect('home')
		elif request.method == 'POST' and request.POST.get('code'):
			user_passcode = request.POST.get('code')
			input_email = request.POST.get('email')
			try:
				user_match = Userdata.objects.get(passcode=user_passcode, email=input_email)
				user_match = 1
			except:
				user_match = 0
			# get passcode from DB
			if user_match: 
				request.session['session_email'] = input_email
				request.session['session_code'] = user_passcode
				return redirect('profile')
			else:
				err_msg = {'err':"The code is incorrect. Please try again.", 'user_email':input_email}
				return render(request, 'auth.html', err_msg)
		else:
			return redirect('home')

		res_email = {'user_email':request.POST.get('email')} 
		return render(request, 'auth.html', res_email)

# logout page 	
def logout(request):
	try:
		del request.session['session_email']
		del request.session['session_code']
	except:
		pass
	return redirect('home') 
	
# delete account 
def delete_acc(request):
	try:
		Userdata.objects.filter(email = request.session.get('session_email')).delete()
		del request.session['session_email']
		del request.session['session_code']
	except Exception as e:
		return HttpResponse(str(e))
	return redirect('home') 

# profile page
def profile(request):
	if request.session.has_key('session_email') and request.session.has_key('session_code'):
		try:
			user_match = Userdata.objects.get(email = request.session.get('session_email'), passcode = request.session.get('session_code'))
		except:
			return redirect('logout') 
		res_data = {'user_email':request.session.get('session_email'), 'user_note':user_match.content}
		if request.method == 'GET':
			return render(request, 'profile.html', res_data)
		elif request.method == 'POST' and request.POST.get('note'):
			new_data = request.POST.get('note')
			Userdata.objects.select_for_update().filter(email=request.session.get('session_email'), passcode=request.session.get('session_code')).update(content=new_data)
			return redirect('profile')
		else:
			return render(request, 'profile.html', res_data)
			
	else:
		return redirect('home')
		