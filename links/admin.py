from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Link, LogoImage, Category

# Register your models here.

class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_by', 'team')


class LogoImageAdmin(admin.ModelAdmin):
    list_display = ('domain', 'image')

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Link, LinkAdmin)
admin.site.register(LogoImage, LogoImageAdmin)
admin.site.register(Category, CategoriesAdmin)