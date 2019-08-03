from django.contrib import admin

# Register your models here.
from .models import Txt,Tag

admin.site.register(Txt)
admin.site.register(Tag)