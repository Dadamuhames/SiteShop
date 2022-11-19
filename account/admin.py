from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import Permission
from django.contrib.sessions.models import Session
# Register your models here.
admin.site.register(Profile)
admin.site.register(Permission)