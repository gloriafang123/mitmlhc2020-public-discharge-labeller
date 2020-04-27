from django.shortcuts import render

# Create your views here.

from .models import TestApp
from .forms import MyForm

def test_app_view(r, *args, **kwargs):
	obj = TestApp.objects.get(id=1)
	# context = {
	# 'field': obj.field1,
	# }
	form = MyForm()
	print("request", r)
	if r.method == "POST":
		print("post!!!")
		form = MyForm(r.POST)
		if form.is_valid():
			print("cleaned form", form.cleaned_data)
			TestApp.objects.create(field1=form.cleaned_data.get('title'))
		else:
			print("errors in form", form.errors)
	else:
		print("not a POST method")
	context={
		'object': obj, # so that we don't have to map out everything, when keys change
		'form':form,
	}
	#print ("field 1 of object", obj.field1)
	return render(r, 'testTemplates/testTemp.html', context)
	# this is still relative to templates directory!!