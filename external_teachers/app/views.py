#App views

from django.shortcuts import render

from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import fenix

import os

fenixAPI = fenix.FenixAPISingleton()
def_password = '0'

# Entry point
def index(request):
	url = fenixAPI.get_authentication_url()
	code = request.GET.get('code')
	name = ''

	if code and not request.user.is_authenticated():
		fenixAPI.set_code(code)
		person = fenixAPI.get_person()
		username = person['username']
		email = person['email']
		user = authenticate(username=username, password=def_password)
		#User doesn't exist
		if user is None:
			#Create the user
			user = User.objects.create_user(username, email, def_password)
			user = authenticate(username=username, password=def_password)

		if user is not None:
			if user.is_active:
				name = person['name']
				login(request, user)
	
	if request.user.is_authenticated():
		person = fenixAPI.get_person()
		name = person['name']

	context = {'auth_url': url, 'name' : name}

	return render(request, 'app/index.html', context)

def about(request):
	about = fenixAPI.get_about()
	context = {'about' : about['institutionName']}
	return render(request, 'app/about.html', context)

def user_logout(request):
	logout(request)
	return index(request)

def sc(request):
	context = {}
	return render(request, 'app/sc.html', context)

def dep(request):
	context = {}
	return render(request, 'app/dep.html', context)

