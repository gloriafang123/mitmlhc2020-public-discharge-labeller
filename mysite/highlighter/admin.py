from django.contrib import admin

# Register your models here.
from .models import SummaryEntry, LabelType

admin.site.register(SummaryEntry)
#use this so that i can see database in the admin for debugging purposes