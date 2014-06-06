# -*- coding: utf-8 -*-
#App views

# Http response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from app.models import ExternalTeacher, FenixAPIUserInfo, Semester

# Form widgets
from django.forms import ModelForm, Textarea, Select, TextInput

# Internationalization
from django.utils.translation import ugettext_lazy as _

# Utils
from datetime import datetime
import csv
import os
from django.core import serializers

import fenixedu

fenixAPI = fenixedu.FenixEduAPISingleton()
def_password = '0'

JSON_FILE = 'departmentMembers_prod.json'

ENCODING = 'utf-8'

EXPORT_ACTION = 'export_action'
CLOSE_ACTION = 'close_action'
DELETE_ACTION = 'delete_action'

POSSIBLE_ACTIONS = {
	'dep_opened' : {EXPORT_ACTION : True,
									CLOSE_ACTION : False,
									DELETE_ACTION : True},
	'dep_closed' : {EXPORT_ACTION : True,
									CLOSE_ACTION : False,
									DELETE_ACTION : False},
	'sc_opened' : {EXPORT_ACTION : True,
									CLOSE_ACTION : True,
									DELETE_ACTION : True},
	'sc_closed' : {EXPORT_ACTION : True,
									CLOSE_ACTION : False,
									DELETE_ACTION : True},
}

# Helper functions:
def process_action(request, template, external_teachers, view):
	saved = False

	if request.POST['action'] == 'close':
		ids = request.POST.getlist('external_teachers')
		ids_park = request.POST.getlist('park')
		ids_card = request.POST.getlist('card')
		if ids:
			# Close proposals
			for et_id in ids:
				e_teacher = ExternalTeacher.objects.get(id = et_id)
				# Check if authorization to use the park was given
				if et_id in ids_park:
					e_teacher.park = True
				# Check if authorization to use the card was given
				if et_id in ids_card:
					e_teacher.card = True
				# Change professional category
				pro_category = request.POST.getlist('professional_category' + et_id)
				e_teacher.professional_category = pro_category[0]
				e_teacher.close()
				e_teacher.save()
			saved = True
			context = get_context_for_list(external_teachers, view)
			context['saved'] = saved
			return render(request, 'app/sc_opened.html', context)

	elif request.POST['action'] == 'export':
		# Create the HttpResponse object with the appropriate CSV header.
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="proposals.csv"'
		writer = csv.writer(response, delimiter=';')

		ids = request.POST.getlist('external_teachers')

		if ids:
			for et_id in ids:
				e_teacher = ExternalTeacher.objects.get(id = et_id)
				if e_teacher.park:
					park = _('True')
				else:
					park = _('False')

				if e_teacher.card:
					card = _('True')
				else:
					card = _('False')
				writer.writerow([
					e_teacher.ist_id,
					e_teacher.get_professional_category_display().encode(ENCODING),
					e_teacher.hours_per_week,
					park.encode(ENCODING),
					card.encode(ENCODING),
					e_teacher.department.encode(ENCODING)
					])

			return response

	elif request.POST['action'] == 'export_all_fields':
			# Create the HttpResponse object with the appropriate CSV header.
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="proposals.csv"'
		writer = csv.writer(response, delimiter=';')

		ids = request.POST.getlist('external_teachers')

		if ids:
			# Write the headers
			writer.writerow([_('Id').encode(ENCODING),
				_('Professional category').encode(ENCODING),
				_('Hours per week').encode(ENCODING),
				_('Park').encode(ENCODING),
				_('Card').encode(ENCODING),
				_('Department').encode(ENCODING),
				_('Name').encode(ENCODING),
				_('Degree').encode(ENCODING),
				_('Course').encode(ENCODING),
				_('Course manager').encode(ENCODING),
				_('Costs Center').encode(ENCODING),
				_('Notes').encode(ENCODING)])
			for et_id in ids:
				e_teacher = ExternalTeacher.objects.get(id = et_id)
				if e_teacher.park:
					park = _('True')
				else:
					park = _('False')

				if e_teacher.card:
					card = _('True')
				else:
					card = _('False')
				writer.writerow([
					e_teacher.ist_id,
					e_teacher.get_professional_category_display().encode(ENCODING),
					e_teacher.hours_per_week,
					park.encode(ENCODING),
					card.encode(ENCODING),
					e_teacher.department.encode(ENCODING),
					e_teacher.name.encode(ENCODING),
					e_teacher.degree.encode(ENCODING),
					e_teacher.course.encode(ENCODING),
					e_teacher.course_manager.encode(ENCODING),
					e_teacher.costs_center.encode(ENCODING),
					e_teacher.notes.encode(ENCODING)
					])

			return response

	elif request.POST['action'] == 'delete':
		ids = request.POST.getlist('external_teachers')
		if ids:
			# Delete proposals
			for et_id in ids:
				e_teacher = ExternalTeacher.objects.get(id = et_id)
				e_teacher.delete()

	context = get_context_for_list(external_teachers, view)
	context['saved'] = saved
	return render(request, template, context)

import json

def open_json_file(filename):
	json_data = open(filename)
	print(json_data)
	data = json.load(json_data)
	return data

def get_departments(username, data):
	department_members = data['departmentMembers']

	for member in department_members:
		if username == member["username"]:
			return member["departments"]

	return None

def is_scientific_council_member(username, data):
	scientific_council_members = data["scientificCouncilMembers"]

	for member in scientific_council_members:
		if username == member["username"]:
			return True

	return False

def is_admin(username, data):
	admins = data['admins']

	for member in admins:
		if username == member['username']:
			return True

	return False

def get_all_departments(data):
	department_members = data['departmentMembers']
	departments = []

	for member in department_members:
		for dep in member['departments']:
			if dep not in departments:
				departments.append(dep)
	return departments

def get_user_dep_acronyms(request):
	acronyms = []
	for dep in request.session["departments"]:
		acronyms.append(dep['acronym'])
	return acronyms

# Forms
class ExternalTeacherForm(ModelForm):

	def __init__(self, *args, **kwargs):
		arg = kwargs.pop('request', None)
		super(ExternalTeacherForm, self).__init__(*args, **kwargs)

		session = arg.session
		deps = session['departments']
		choices = [(d['acronym'], d['acronym']) for d in deps]
		self.fields['department'].widget = Select(choices=choices)

		# Labels internationalization
		self.fields['ist_id'].label = _('IST ID')
		self.fields['name'].label = _('name')
		self.fields['semester'].label = _('semester')
		self.fields['hours_per_week'].label = _('hours_per_week')
		self.fields['department'].label = _('department')
		self.fields['degree'].label = _('degree')
		self.fields['course'].label = _('course')
		self.fields['course_manager'].label = _('course_manager')
		self.fields['costs_center'].label = _('costs_center')
		self.fields['notes'].label = _('notes')

	class Meta:
		model = ExternalTeacher
		fields = ['ist_id', 'name', 'semester', 'hours_per_week',
							'department', 'degree', 'course', 'course_manager',
							'costs_center', 'notes']

		widgets = {'notes' : Textarea(), 'name' : TextInput(attrs={'readonly' : 'true'})}

# Entry point
def index(request):
	url = fenixAPI.get_authentication_url()
	code = request.GET.get('code')
	json_data = open_json_file(JSON_FILE)

	if code and not request.user.is_authenticated():
		fenix_user = fenixedu.User()
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
			user.first_name = person['name']
			user.save()
			info.save()

		if user is not None:
			if is_admin(username, json_data):
				departments = get_all_departments(json_data)
			else:
				departments = get_departments(user.username, json_data)

			can_login = False

			if is_admin(username, json_data):
				request.session['departments'] = departments
				request.session['is_department_member'] = True
				request.session['dep_acronyms'] = get_user_dep_acronyms(request)
				request.session['is_scientific_council_member'] = True
				can_login = True

			# Check if it's a department member
			elif departments is not None:
				request.session['departments'] = departments
				request.session['is_department_member'] = True
				request.session['dep_acronyms'] = get_user_dep_acronyms(request)
				can_login = True

			# Check if it's a scientific council member
			if is_scientific_council_member(username, json_data):
				request.session['is_scientific_council_member'] = True
				can_login = True

			if user.is_active and can_login:
				login(request, user)

	context = {'auth_url' : url, 'is_department_member' : 'is_department_member' in request.session,
			'is_scientific_council_member' : 'is_scientific_council_member' in request.session}

	return render(request, 'app/index.html', context)

# Get the name with a given ist id
def name(request):
	name = 'XxxxxXXX áàÁÀ éÉèÈ íìÍÌ óòÓÒ úùÚÙ ãẽĩõũ âêîôû'
	return HttpResponse(name)

# Get the context to return to the views that show a list of external teachers
def get_context_for_list(external_teachers, view):
	context = POSSIBLE_ACTIONS[view]
	context['external_teachers'] = external_teachers
	context['semesters'] = Semester.objects.all()
	context['current_semester'] = Semester.get_or_create_current()
	return context

def get_external_teachers_list(request, is_closed, filter_by_dep):
	semester_param = request.GET.get('semester')

	if filter_by_dep:
		external_teachers = ExternalTeacher.objects.filter(is_closed = is_closed,
												department__in = request.session['dep_acronyms'])
	else:
		external_teachers = ExternalTeacher.objects.filter(is_closed = is_closed)

	if semester_param:
		semester = int(semester_param)
		if semester > 0:
			external_teachers = external_teachers.filter(semester = semester)

	return external_teachers

def about(request):
	about = fenixAPI.get_about()
	context = {'about' : about['institutionName']}
	return render(request, 'app/about.html', context)

def user_logout(request):
	logout(request)
	return index(request)

def sc_opened(request):
	external_teachers = get_external_teachers_list(request, is_closed = False,
																									filter_by_dep = False)
	saved = False
	template = 'app/sc_opened.html'

	if request.method == 'POST':
		return process_action(request, template, external_teachers, 'sc_opened')

	context = get_context_for_list(external_teachers, 'sc_opened')

	context['saved'] = False
	context['pro_categories'] = ExternalTeacher.PROFESSIONAL_CATEGORIES
	return render(request, template, context)

def sc_closed(request):
	template = 'app/sc_closed.html'
	external_teachers = get_external_teachers_list(request, is_closed = True,
																									filter_by_dep = False)

	if request.method == 'POST':
		return process_action(request, template, external_teachers, 'sc_closed')

	context = get_context_for_list(external_teachers, 'sc_closed')
	return render(request, template, context)

def dep_opened(request):
	external_teachers = get_external_teachers_list(request, is_closed = False,
																									filter_by_dep = True)
	template = 'app/dep_opened.html'

	if request.method == 'POST':
		return process_action(request, template, external_teachers, 'dep_opened')

	context = get_context_for_list(external_teachers, 'dep_opened')
	context['can_edit'] = True
	return render(request, template, context)

def dep_closed(request):
	template = 'app/dep_closed.html'
	external_teachers = get_external_teachers_list(request, is_closed = True,
																									filter_by_dep = True)

	if request.method == 'POST':
		return process_action(request, template, external_teachers, 'dep_closed')

	context = get_context_for_list(external_teachers, 'dep_closed')
	return render(request, template, context)

def dep_prop_new(request):
	if request.method == 'POST':
		form = ExternalTeacherForm(request.POST, request=request)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/app/dep_opened/')
	else:
		form = ExternalTeacherForm(request=request)

	context = {'form' : form}
	return render(request, 'app/external_teacher_form.html', context)

def edit(request, pk):
	template = 'app/dep_opened.html'
	external_teacher = ExternalTeacher.objects.get(id=pk)

	# Its not supposed to try to edit a closed one
	if external_teacher.is_closed:
		return render(request, template, {'error' : 'ERROR: This proposal is closed'})

	if request.method == 'POST':
		form = ExternalTeacherForm(request.POST, request=request, instance=external_teacher)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/app/dep_opened/')
	else:
		form = ExternalTeacherForm(request=request, instance=external_teacher)

	context = {'form' : form}
	return render(request, 'app/external_teacher_form.html', context)

def change_park(request, pk):
	value = request.GET.get("value")
	external_teacher = ExternalTeacher.objects.get(id=pk)

	if value == 'true':
		external_teacher.park = True
		response = _('Yes')
	else:
		external_teacher.park = False
		response = _('No')

	external_teacher.save()

	return HttpResponse(response)

def change_card(request, pk):
	value = request.GET.get("value")
	external_teacher = ExternalTeacher.objects.get(id=pk)

	if value == 'true':
		external_teacher.card = True
		response = _('Yes')
	else:
		external_teacher.card = False
		response = _('No')

	external_teacher.save()

	return HttpResponse(response)

def change_professional_category(request, pk):
	value = request.GET.get("value")
	external_teacher = ExternalTeacher.objects.get(id=pk)
	external_teacher.professional_category = value

	external_teacher.save()

	return HttpResponse(external_teacher.get_professional_category_display())

def get_external_teacher(request, pk):
	external_teacher = ExternalTeacher.objects.get(id=pk)
	if external_teacher.close_date:
		close_date = external_teacher.close_date.strftime("%d/%m/%Y %H:%M")
	else:
		close_date = ''
	response = {'id' : external_teacher.id,
							'ist_id' : external_teacher.ist_id,
							'name' : external_teacher.name,
							'semester' : {
														'id' : external_teacher.semester.id,
														'display' : external_teacher.semester.get_display()
														},
							'is_closed' : external_teacher.is_closed,
							'close_date' : close_date,
							'professional_category' : {
																					'key' : external_teacher.professional_category,
																					'display' : external_teacher.get_professional_category_display(),
																				},
							'hours_per_week' : '%.2f' % external_teacher.hours_per_week,
							'park' : external_teacher.park,
							'card' : external_teacher.card,
							'department' : external_teacher.department,
							'degree' : external_teacher.degree,
							'course' : external_teacher.course,
							'course_manager' : external_teacher.course_manager,
							'costs_center' : external_teacher.costs_center,
							'notes' : external_teacher.notes,
						}

	return HttpResponse(json.dumps(response), content_type="application/json")
