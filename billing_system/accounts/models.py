from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.product_name


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=255, unique=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Invoice #{self.invoice_number}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey('Invoice', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2)  # Tax rate as percentage (e.g., 8 for 8%)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

   
    def save(self, *args, **kwargs):
        if self.quantity is None:
            self.quantity = 1  
        if self.rate is None:
            self.rate = 0  
        if self.tax is None:
            self.tax = 0  
       
        self.subtotal = (self.quantity * self.rate) + (self.quantity * self.rate * (self.tax / 100))
        super().save(*args, **kwargs)