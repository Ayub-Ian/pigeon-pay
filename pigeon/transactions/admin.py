from django.contrib import admin
from .models import Transaction, Category, Product, ProductFile

class ProductInline(admin.TabularInline):
    model = Product

class ProductFileInline(admin.TabularInline):
    model = ProductFile



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title','buyer', 'seller']
    inlines = [ProductInline, ProductFileInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

