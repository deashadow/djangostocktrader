from django import forms
from . models import BankAccount #Product  #Stock



#class ProductForm( forms.ModelForm):
 #   class Meta:
  #      model = Product
  #      fields = ['name','price','quantity']
  #      widgets = {
  #          'name': forms.TextInput(
  #              attrs={
  #                  'id':'name'
  #              }
  #          ),
   #         'price': forms.TextInput(
   #             attrs={
   #                 'id':'price'
   #             }
   #         ),
   #         'quantity': forms.TextInput(
   #             attrs={
   #                 'id':'quantity'
   #             }
   #         )
   #     }

class BankAccountForm( forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['balance']
        widgets = {
            'balance': forms.TextInput(
                attrs={
                    'id': 'balance'
                }
            )
        }    

#class StockForm(forms.ModelForm):
#    class Meta:
#        model = Stock
#        fields = ["ticker"]        