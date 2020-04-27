from django.shortcuts import render

# Create your views here.

from .models import TestApp
def test_app_view(r, *args, **kwargs):
	obj = TestApp.objects.get(id=1)
	# context = {
	# 'field': obj.field1,
	# }
	context={
		'object': obj, # so that we don't have to map out everything, when keys change
	}
	print (obj.field1)
	return render(r, 'testTemplates/testTemp.html', context)
	# this is still relative to templates directory!!