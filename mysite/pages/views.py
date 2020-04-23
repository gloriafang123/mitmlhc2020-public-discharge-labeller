from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home_view(r, *args, **kwargs): #first argument required.
	print("request", r, args, kwargs)
	return HttpResponse("<h1> Hello world</h1>")

def other_view(r, *args, **kwargs):
	print("request", r, args, kwargs) #r is a WSGI request, can check request.user etc info
	return render(r, "other_view.html", {'variable': 123, 'variable2': "variable2"}) #knows this from templates.