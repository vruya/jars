from django.db import models

import datetime

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=8, default=0)

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    products = models.ManyToManyField(Product, related_name='categories') 

class Order(models.Model):
    ordered_at = models.DateTimeField(auto_now_add=True) #
    customer_name = models.CharField(max_length=50)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)   
    quantity = models.PositiveIntegerField(default=0)