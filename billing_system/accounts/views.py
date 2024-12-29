from django.shortcuts import render,redirect,get_object_or_404
from.models import *
from.forms import *
from django.db.models import Q
from django.forms import modelformset_factory
from django.db.models import Sum
from django.utils.timezone import now






def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'customer_form.html', {'form': form})    



def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()  
            return redirect('customer_list')  
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customer_form.html', {'form': form, 'customer': customer})  


def customer_list(request):
    query = request.GET.get('q', '')  
    customers = Customer.objects.all()

    
    if query:
        customers = customers.filter(
            models.Q(name__icontains=query) |
            models.Q(phone_number__icontains=query) |
            models.Q(email__icontains=query)
        )

    return render(request, 'customer_list.html', {'customers': customers, 'query': query})         
    
                 # product


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})



def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})   



def search_products(request):
    query = request.GET.get('q', '')  
    products = Product.objects.all()  

    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(rate__icontains=query) |
            Q(tax_percentage__icontains=query)
        )

    return render(request, 'product_list.html', {'products': products, 'query': query})
    
def product_list(request):
    products = Product.objects.all() 
    return render(request, 'product_list.html', {'products': products})    

    
    
              # invoice


def generate_invoice_number():
    last_invoice = Invoice.objects.last()
    if last_invoice:
        last_number_str = last_invoice.invoice_number.split('-')[-1]
        last_number = int(last_number_str.lstrip('INV'))
        new_number = last_number + 1
        return f"INV{new_number:06d}"
    return "INV000001"

def invoice_create(request):
    InvoiceItemFormSet = modelformset_factory(InvoiceItem, form=InvoiceItemForm, extra=1)

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        item_formset = InvoiceItemFormSet(request.POST)

        if invoice_form.is_valid() and item_formset.is_valid():
            
            invoice = invoice_form.save(commit=False)
            invoice.invoice_number = generate_invoice_number()
            invoice.date = now().date()  
            invoice.save()

            
            for item_form in item_formset:
                item = item_form.save(commit=False)
                item.invoice = invoice
                item.save()  

           
            total_amount = invoice.items.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
            invoice.total_amount = round(total_amount, 2) 
            invoice.save()

            return redirect('invoice_list')
    else:
        invoice_form = InvoiceForm()
        item_formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.none())

    return render(request, 'invoice_create.html', {
        'invoice_form': invoice_form,
        'item_formset': item_formset,
        'customers': Customer.objects.all(),
        'products': Product.objects.all()
    })





def invoice_list(request):
    invoices = Invoice.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        invoices = invoices.filter(invoice_number__icontains=search_query)
    for invoice in invoices:
       
        total_amount = invoice.items.aggregate(Sum('subtotal'))['subtotal__sum']
        invoice.total_amount = total_amount if total_amount else 0  

    return render(request, 'invoice_list.html', {'invoices': invoices})
