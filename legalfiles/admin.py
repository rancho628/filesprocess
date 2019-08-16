from django.contrib import admin

# Register your models here.
from .models import Txt,Tag
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import User

admin.site.register(User)
admin.site.register(Txt)
admin.site.register(Tag)
