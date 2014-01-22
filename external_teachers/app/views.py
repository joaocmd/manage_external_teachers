#App views

from django.shortcuts import render

from django.http import HttpResponse

# Entry point
def index(request):
	context = {}
	return render(request, 'app/index.html', context)

