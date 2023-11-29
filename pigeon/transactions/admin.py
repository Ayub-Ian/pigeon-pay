from django.contrib import admin
from .models import Transaction, Category



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title','buyer', 'seller']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
