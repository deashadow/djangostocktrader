from django.contrib import admin
from .models import BankAccount, Product, Stock
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')

admin.site.register(Product, ProductAdmin)



class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank_balance', 'created')

admin.site.register(BankAccount, BankAccountAdmin)

admin.site.register(Stock)