from django import forms
from . models import BankAccount, Stock #Product  



#class ProductForm( forms.ModelForm):
 #   class Meta:
  #      model = Product
  #      fields = ['name','price','quantity']
  #      widgets = {
  #          'name': forms.TextInput(
  #              attrs={
  #                  'id':'name_id'
  #              }
  #          ),
   #         'price': forms.TextInput(
   #             attrs={
   #                 'id':'price_id'
   #             }
   #         ),
   #         'quantity': forms.TextInput(
   #             attrs={
   #                 'id':'quantity_id'
   #             }
   #         )
   #     }

class BankAccountForm( forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["user", "bank_balance", "symbol", "current_price", "quantity"]
        widgets = {
            'user': forms.TextInput(
                attrs={
                    'id':'user_id'
                }
            ),
            'bank_balance': forms.TextInput(
                attrs={
                    'id':'balance_id'
               }
            ),
            'symbol': forms.TextInput(
                attrs={
                    'id':'symbol_id'
                }
            ),
            'current_price': forms.TextInput(
                attrs={
                    'id':'current_price_id'
                }
            ),
            'quantity': forms.TextInput(
                attrs={
                    'id':'quantity_id'
                }
            )
        } 
        
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker"]        