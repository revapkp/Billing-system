from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_customer, name='add_customer'),
    path('edit/<int:customer_id>/',views.edit_customer,name = 'edit_customer'),
    path('customer-list/', views.customer_list, name='customer_list'),
    path('', views.product_list, name='product_list'),
    path('addproduct/', views.add_product, name='add_product'),
    path('editproduct/<int:product_id>/', views.edit_product, name='edit_product'),
    path('search/', views.search_products, name='search_products'),
    path('create/', views.invoice_create, name='invoice_create'),
    path('list/', views.invoice_list, name='invoice_list'),
   
    
]