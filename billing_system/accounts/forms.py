from django import forms
from .models import *

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','phone_number','email']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =['product_name','rate','tax_percentage']
   