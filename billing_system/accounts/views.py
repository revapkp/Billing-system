from django.shortcuts import render,redirect,get_object_or_404
from.models import *
from.forms import *





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
    
