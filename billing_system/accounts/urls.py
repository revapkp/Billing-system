from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_customer, name='add_customer'),
    path('edit/<int:customer_id>/',views.edit_customer,name = 'edit_customer'),
    path('customer-list/', views.customer_list, name='customer_list'),
    
]