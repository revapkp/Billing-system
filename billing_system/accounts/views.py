from django.shortcuts import render,redirect,get_object_or_404
from.models import *
from.forms import *
from django.db.models import Q






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
            form.save()  # Update the existing customer
            return redirect('customer_list')  # Redirect to the customer list page
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customer_form.html', {'form': form, 'customer': customer})  


def customer_list(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    customers = Customer.objects.all()

    # Filter customers by name, phone number, or email
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
            return redirect('product_list')  # Redirect to the product list after adding
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})



def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to the product list after editing
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})   



def search_products(request):
    query = request.GET.get('q', '')  # Get the search query from the URL parameter
    products = Product.objects.all()  # Start with all products

    if query:
        # Use Q objects to combine multiple conditions with OR logic
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(rate__icontains=query) |
            Q(tax_percentage__icontains=query)
        )

    return render(request, 'product_list.html', {'products': products, 'query': query})
    
def product_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'product_list.html', {'products': products})    