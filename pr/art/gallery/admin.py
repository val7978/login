from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Work, PasswordResetToken

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_author', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('is_author', 'phone', 'portfolio')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Work)
admin.site.register(PasswordResetToken)
