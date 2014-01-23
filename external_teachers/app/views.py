#App views

from django.shortcuts import render

from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import fenix

import os

fenixAPI = fenix.FenixAPISingleton()
def_password = '0'

# Entry point
def index(request):
	url = fenixAPI.get_authentication_url()
	code = request.GET.get('code')
	login_success = False
	name = ''

	if code and not request.user.is_authenticated():
		fenixAPI.set_code(code)
		print(code and not request.user.is_authenticated())
		person = fenixAPI.get_person()
		username = person['istId']
		email = person['email']
		user = authenticate(username=username, password=def_password)
		#User doesn't exist
		if user is None:
			#Create the user
			user = User.objects.create_user(username, email, def_password)
			user = authenticate(username=username, password=def_password)

		if user is not None:
			if user.is_active:
				login_success = True
				name = person['name']
				login(request, user)

	context = {'auth_url': url, 'login_success' : request.user.is_authenticated(), 'name' : name}

	return render(request, 'app/index.html', context)

def about(request):
	about = fenixAPI.get_about()
	context = {'about' : about['institutionName']}
	return render(request, 'app/about.html', context)
