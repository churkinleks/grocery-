from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from apps.user.models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_superuser')
    fields = ('username', 'email', 'is_superuser')
    fieldsets = None
    search_fields = ('username',)
    show_full_result_count = False
