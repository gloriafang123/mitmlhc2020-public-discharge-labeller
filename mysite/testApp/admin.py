from django.contrib import admin

# Register your models here.
from .models import TestApp

admin.site.register(TestApp)