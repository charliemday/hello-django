from django.contrib import admin
from .models import Team

# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'description', 'created_by')

admin.site.register(Team, TeamAdmin)