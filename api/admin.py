from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CreditCard


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin with profile fields"""
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('name', 'home_address')}),
    )


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    """Credit Card Admin"""
    list_display = ['cardholder_name', 'user', 'card_number', 'is_default', 'created_at']
    list_filter = ['is_default', 'created_at']
    search_fields = ['user__username', 'cardholder_name']
    readonly_fields = ['created_at', 'updated_at']
