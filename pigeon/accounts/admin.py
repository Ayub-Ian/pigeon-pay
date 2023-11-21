from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'is_verified']
    search_fields = ['email']
    list_filter = ['phone', 'email', 'is_verified']
