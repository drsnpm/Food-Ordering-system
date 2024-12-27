from django.db import models
import datetime

class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200,default='',null=True, blank=True)
    image = models.ImageField(upload_to='uploads/image')

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    uname = models.CharField(max_length=20)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    mobile = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for {self.quantity} {self.product.name} by {self.customer.name}"
