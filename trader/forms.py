from django import forms
from . models import BankAccount, Stock, StockProduct  



class StockProductForm( forms.ModelForm):
    class Meta:
        model = StockProduct
        fields = ['name','price','quantity']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'id':'name_id'
                }
            ),
            'price': forms.TextInput(
                attrs={
                    'id':'price_id'
                }
            ),
            'quantity': forms.TextInput(
                attrs={
                    'id':'quantity_id'
                }
            )
        }

class BankAccountForm( forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["user", "bank_balance"]
        widgets = {
            'user': forms.TextInput(
                attrs={
                    'id':'user_id'
                }
            ),
            'bank_balance': forms.TextInput(
                attrs={
                    'id':'bank_balance_id'
               }
            )
            
        } 
        
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker"]        