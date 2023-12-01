from django.contrib import admin
from .models import Transaction, Category, Product

class ProductInline(admin.TabularInline):
    model = Product




@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title','buyer', 'seller']
    inlines = [ProductInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

