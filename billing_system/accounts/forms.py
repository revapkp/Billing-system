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
   
from django import forms
from .models import Invoice, InvoiceItem

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the customer field with the 'search' functionality
        self.fields['customer'].queryset = Customer.objects.all()


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'rate', 'tax', 'subtotal']

    
   
class InvoiceItemFormSet(forms.BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            if form.cleaned_data.get('product') and form.cleaned_data.get('quantity') <= 0:
                raise forms.ValidationError("Quantity must be greater than 0.")
