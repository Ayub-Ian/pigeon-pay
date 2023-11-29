from django.contrib import admin
from .models import User, Buyer, Seller

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'is_verified']
    search_fields = ['email']
    list_filter = ['phone', 'email', 'is_verified']


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['user']
   
@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['user']
   