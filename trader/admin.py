from django.contrib import admin
from .models import BankAccount, StockProduct, Stock
# Register your models here.

class StockProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')

admin.site.register(StockProduct, StockProductAdmin)



class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank_balance', 'created')

admin.site.register(BankAccount, BankAccountAdmin)

admin.site.register(Stock)