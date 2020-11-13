from django import forms
from . models import Product



class ProductForm( forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','quantity']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'id':'name'
                }
            ),
            'price': forms.TextInput(
                attrs={
                    'id':'price'
                }
            ),
            'quantity': forms.TextInput(
                attrs={
                    'id':'quantity'
                }
            )
        }