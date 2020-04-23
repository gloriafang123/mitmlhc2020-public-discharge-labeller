from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home_view(r, *args, **kwargs): #first argument required.
	return HttpResponse("<h1> Hello world</h1>")

def other_view(r, *args, **kwargs):
	return HttpResponse("<h1> Other View </h1>")