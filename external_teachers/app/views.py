#App views

from django.shortcuts import render

from django.http import HttpResponse

import fenix

import os

fenixAPI = fenix.FenixAPISingleton()

# Entry point
def index(request):
	url = fenixAPI.get_authentication_url()
	context = {'auth_url': url}
	return render(request, 'app/index.html', context)

def about(request):
	about = fenixAPI.get_about()
	context = {'about' : about['institutionName']}
	return render(request, 'app/about.html', context)
