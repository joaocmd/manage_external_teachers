#App views

from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from app.models import ExternalTeacher, ExternalTeacherForm

from datetime import datetime

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
		response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
		writer = csv.writer(response)
		
		ids = request.POST.getlist('external_teachers')

		for et_id in ids:
			e_teacher = ExternalTeacher.objects.get(id = et_id)	
			writer.writerow([e_teacher.user.username, e_teacher.name])
		
		return response
	
	context = {'external_teachers' : external_teachers, 'saved' : saved, 'close_action' : close_action, 'export_action' : export_action}
	return render(request, 'app/sc_opened.html', context)


# Entry point
def index(request):
	url = fenixAPI.get_authentication_url()
	code = request.GET.get('code')

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
			name = person['name']
			user.first_name = name
			user.save()

		if user is not None:
			if user.is_active:
				login(request, user)
	
	context = {'auth_url': url}

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
	export_action = True
	external_teachers = ExternalTeacher.objects.filter(is_closed = True)
	
	context = {'external_teachers' : external_teachers, 'export_action' : export_action}
	return render(request, 'app/sc_closed.html', context)

def dep_opened(request):
	external_teachers = ExternalTeacher.objects.filter(is_closed = False)
	export_action = True

	context = {'external_teachers' : external_teachers, 'export_action' : export_action}
	return render(request, 'app/dep_opened.html', context)

def dep_closed(request):
	export_action = True
	external_teachers = ExternalTeacher.objects.filter(is_closed = True)
	
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

