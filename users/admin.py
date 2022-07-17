from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .models import User, UserFeedback

class CustomUserAdmin(UserAdmin):
    pass

class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback', 'created', "resolved")

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserFeedback, UserFeedbackAdmin)