from django.shortcuts import render

# Create your views here.

import highlighter.backend as backend
from .models import SummaryEntry, LabelType
from .form import SummaryForm


def highlighter_view(r, *args, **kwargs):
	"""
	main discharge summary labeller view
	"""

	#vars: cleaned_data, labels
	processed_text = "(Enter summary to see labels.)"
	form = SummaryForm()
	if r.method == "POST":
		form = SummaryForm(r.POST)
		if form.is_valid():
			cleaned_data = form.cleaned_data
			labels = cleaned_data.pop('labels')
			s = SummaryEntry.objects.create(**cleaned_data)
			s.labels.set(labels)

			# if using ML model, use backend.get_summary() function instead.
			processed_text = backend.get_summary_scispacy(cleaned_data, labels)
			s.processed = processed_text
			s.save() #this step is key!!! :) saves it!

		else:
			print ("Post:", r.POST, form.is_valid())
			form = SummaryForm()
			print("Errors in form:", form.errors)
	else:
		print("Not a POST method.")

	context={
		'form':form,
		'processed_text': processed_text,
	}
	return render(r, 'highlighter_temp.html', context)
	# this is still relative to templates directory!!
