from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Link

# Register your models here.

class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_by', 'team')



admin.site.register(Link, LinkAdmin)