from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    exclude = ('password',)


admin.site.register(User, CustomUserAdmin)
