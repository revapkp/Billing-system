from django.db import models



# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.product_name

# Invoice Model
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=255, unique=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Invoice #{self.invoice_number}"

# InvoiceItem Model (for line items in an invoice)
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.subtotal = (self.quantity * self.rate) + (self.quantity * self.rate * self.tax / 100)
        super().save(*args, **kwargs)

