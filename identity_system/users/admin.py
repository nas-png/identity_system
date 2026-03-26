from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['unique_id', 'first_name', 'last_name', 'email', 'phone_number', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'unique_id']
    readonly_fields = ['unique_id', 'internal_hash', 'created_at', 'updated_at']