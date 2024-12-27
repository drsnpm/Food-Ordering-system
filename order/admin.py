from django.contrib import admin
from .models import Product, Category, Customer, Order


class AdminCategories(admin.ModelAdmin):
    list_display = ['name'] 

class AdminProducts(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class AdminCustomer(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile', 'uname', 'password']

class AdminOrders(admin.ModelAdmin):
    list_display = ['product', 'customer', 'quantity', 'price','address', 'mobile', 'date']

admin.site.register(Category, AdminCategories)
admin.site.register(Product, AdminProducts)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Order, AdminOrders)
