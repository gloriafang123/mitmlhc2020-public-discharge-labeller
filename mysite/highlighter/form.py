from django.forms import ModelForm
from django import forms
from highlighter.models import SummaryEntry, LabelType


LABELS = [
("label1", "Label1"),
("label2", "Label2"),
("label3", "Label3"),
]
class SummaryForm(ModelForm):
	title = forms.CharField(label = "",  #label affects its rendering
		widget = forms.TextInput(attrs={
			"placeholder":"Insert title here",
			"class": "title-form-class",
			}
			))
	original = forms.CharField(label = "",  #label affects its rendering
		widget = forms.Textarea(attrs={
			"placeholder":"Insert discharge summary here",
			"class": "summary-form-class materialize-textarea",
			}
			))
	labels = forms.ModelMultipleChoiceField(
		label="Select all relevant labels",
		queryset=LabelType.objects.all(),
		widget = forms.CheckboxSelectMultiple,
		required=False,
		)
	#,	empty_label = "(Select all relevant labels)",)#,  #label affects its rendering
		#widget = forms.SelectMultiple, 
		#choices = LABELS)

	class Meta:
		model = SummaryEntry
		fields = ["title", "original", "labels"] # not render "processed"

class LabelType(ModelForm):
	class Meta:
		model = LabelType
		fields = ["label"]
