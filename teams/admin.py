from django.contrib import admin
from .models import Team, TeamMember, TeamInvite

# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'description', 'created_by')

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team', 'user', 'is_active')

class TeamInviteAdmin(admin.ModelAdmin):
    list_display = ('team', 'email', 'token')


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(TeamInvite, TeamInviteAdmin)