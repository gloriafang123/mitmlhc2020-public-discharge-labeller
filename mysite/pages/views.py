from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home_view(r, *args, **kwargs): #first argument required.
	print("request", r, args, kwargs)
	return HttpResponse("<h1> Hello world</h1>")

def other_view(r, *args, **kwargs):
	context = {'variable': 123, 
	'variable2': "variable2",
	'listitem': [1,2,3]}

	# try to change if statements in view (context), not so much logic in render

	print("request", r, args, kwargs) #r is a WSGI request, can check request.user etc info
	return render(r, "other_view.html", 
	context) #knows this from templates.
	# can go into any of the templates rendered, not have to be other_view, can be include.html also