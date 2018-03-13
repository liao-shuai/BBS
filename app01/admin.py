# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import BBS, BBS_user, Category

from models import Profile


class BBSAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'ranking' )
    list_filter = ('author', 'category', )
    search_fields = ('title', 'created_at', 'author__user__username')

class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'signature')
    list_filter = ('user', )
    search_fields = ('user',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'administrator')
    list_filter = ('name', )
    search_fields = ('name',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', )
    search_fields = ('name',)

admin.site.register(BBS, BBSAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BBS_user, UserAdmin)
admin.site.register(Profile, ProfileAdmin)

# Register your models here.
