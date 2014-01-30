#App views

from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from app.models import ExternalTeacher, ExternalTeacherForm, FenixAPIUserInfo

from datetime import datetime

import csv

import fenix

import os

fenixAPI = fenix.FenixAPISingleton()
def_password = '0'

# Helper functions:
def process_action(request, external_teachers, close_action, export_action):
	saved = False
	
	if request.POST['action'] == 'close':
		ids = request.POST.getlist('external_teachers')	
		if ids:
			for et_id in request.POST.getlist('external_teachers'):
				e_teacher = ExternalTeacher.objects.get(id = et_id)
				e_teacher.close_date = datetime.now()
				e_teacher.is_closed = True
				e_teacher.save()
			saved = True
			context = {'external_teachers' : external_teachers, 'saved' : saved, 'close_action' : close_action, 'export_action' : export_action}
			return render(request, 'app/sc_opened.html', context)

	elif request.POST['action'] == 'export':
		# Create the HttpResponse object with the appropriate CSV header.
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="proposals.csv"'
		writer = csv.writer(response)
		
		ids = request.POST.getlist('external_teachers')

		if ids:
			for et_id in ids:
				e_teacher = ExternalTeacher.objects.get(id = et_id)	
				writer.writerow([e_teacher.user.username, e_teacher.name])
		
			return response
	
	context = {'external_teachers' : external_teachers, 'saved' : saved, 'close_action' : close_action, 'export_action' : export_action}
	return render(request, 'app/sc_opened.html', context)

import json

def open_json_file(filename):
	json_data = open(filename)
	print(json_data)
	data = json.load(json_data)
	return data

def get_departments(username):
	data = open_json_file('authorized.json')
	department_members = data['departmentMembers']

	for member in department_members:
		if username == member["username"]:
			return member["departments"]

	return None

def is_scientific_council_member(username):
	data = open_json_file('authorized.json')
	scientific_council_members = data["scientificCouncilMembers"]

	for member in scientific_council_members:
		if username == member["username"]:
			return True
	
	return False

# Entry point
def index(request):
	url = fenixAPI.get_authentication_url()
	code = request.GET.get('code')

	if code and not request.user.is_authenticated():
		fenix_user = fenix.User()
		fenixAPI.set_code(code, user=fenix_user)
		person = fenixAPI.get_person(fenix_user)
		username = person['username']
		email = person['email']
		user = authenticate(username=username, password=def_password)
		#User doesn't exist
		if user is None:
			#Create the user
			user = User.objects.create_user(username, email, def_password)
			info = FenixAPIUserInfo(code=fenix_user.code, access_token=fenix_user.access_token, refresh_token=fenix_user.refresh_token, token_expires=fenix_user.token_expires, user=user)
			user = authenticate(username=username, password=def_password)
			user.first_name = name
			user.save()
			info.save()

		if user is not None:
			departments = get_departments(user.username)
			can_login = False
			# Check if it's a department member
			if departments is not None:
				request.session['departments'] = departments
				request.session['is_department_member'] = True
				can_login = True
			
			# Check if it's a scientific council member
			if is_scientific_council_member(username):
				request.session['is_scientific_council_member'] = True
				can_login = True

			if user.is_active and can_login:
				login(request, user)
	
	context = {'auth_url' : url, 'is_department_member' : 'is_department_member' in request.session, 'is_scientific_council_member' : 'is_scientific_council_member' in request.session}

	return render(request, 'app/index.html', context)

def about(request):
	about = fenixAPI.get_about()
	context = {'about' : about['institutionName']}
	return render(request, 'app/about.html', context)

def user_logout(request):
	logout(request)
	return index(request)

def sc_opened(request):
	external_teachers = ExternalTeacher.objects.filter(is_closed = False)
	saved = False
	close_action = True
	export_action = True

	if request.method == 'POST':
		return process_action(request, external_teachers, close_action, export_action)
	context = {'external_teachers' : external_teachers, 'saved' : saved, 'close_action' : close_action, 'export_action' : export_action}
	return render(request, 'app/sc_opened.html', context)

def sc_closed(request):
	close_action = False
	export_action = True
	external_teachers = ExternalTeacher.objects.filter(is_closed = True)

	if request.method == 'POST':
		return process_action(request, external_teachers, close_action, export_action)

	context = {'external_teachers' : external_teachers, 'export_action' : export_action}
	return render(request, 'app/sc_closed.html', context)

def dep_opened(request):
	external_teachers = ExternalTeacher.objects.filter(is_closed = False)
	close_action = False
	export_action = True

	if request.method == 'POST':
		return process_action(request, external_teachers, close_action, export_action)

	context = {'external_teachers' : external_teachers, 'export_action' : export_action}
	return render(request, 'app/dep_opened.html', context)

def dep_closed(request):
	close_action = False
	export_action = True
	external_teachers = ExternalTeacher.objects.filter(is_closed = True)
	
	if request.method == 'POST':
		return process_action(request, external_teachers, close_action, export_action)

	context = {'external_teachers' : external_teachers, 'export_action' : export_action}
	return render(request, 'app/dep_closed.html', context)

def dep_prop_new(request):
	if request.method == 'POST':
		form = ExternalTeacherForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/app/dep_opened/')
	else:
		form = ExternalTeacherForm()

	context = {'form' : form}
	return render(request, 'app/dep_prop_new.html', context)

