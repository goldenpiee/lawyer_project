from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LawyerProfile

class CustomUserAdmin(UserAdmin):
    # Убираем все упоминания username
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('full_name', 'phone')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone', 'password1', 'password2', 'is_staff'),
        }),
    )
    list_display = ('email', 'full_name', 'phone', 'is_staff')
    search_fields = ('email', 'full_name', 'phone')
    ordering = ('email',)
    
@admin.register(LawyerProfile)
class LawyerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']
    # Update search field to use email since CustomUser lacks 'username'
    search_fields = ['user__email']

admin.site.register(CustomUser, CustomUserAdmin)