from django.db import models
from django.db.models import fields

class Category(models.Model):
    name = fields.CharField(max_length=50)
    description = fields.TextField()
    image = fields.ImageField(max_lenght=255, null=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = fields.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = fields.DecimalField(max_digits=7, decimal_places=2)
    availability = fields.PositiveSmallIntegerField()
    image = fields.ImageField(upload_to=..., max_lenght=255, null=True)
    discount = fields.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.name)


class Basket(models.Model):
    price = fields.DecimalField(max_digits=7, decimal_places=2)
    discount = fields.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.price)


class Shopping_Cart(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = fields.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.basket)


class Buyer(models.Model):
    user = fields.
    discount = fields.PositiveSmallIntegerField()
    phone = fields.

    def __str__(self):
        return str(self.discount)


class Delivery(models.Model):
     method = fields.CharField(max_length=20)

     def __str__(self):
         return str(self.method)


class Address(models.Model):
    country = fields.CharField(max_length=50)
    city = fields.CharField(max_length=30)
    street = fields.CharField(max_length=40)
    house = fields.CharField(max_length=5)
    building = fields.PositiveSmallIntegerField()
    flat = fields.PositiveSmallIntegerField()
    index = fields.CharField(max_length=6)

    def __str__(self):
        return str(self.country)


class Status(models.Model):
    status = fields.CharField(max_length=45)

    def __str__(self):
        return str(self.status)

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    price = fields.DecimalField(max_digits=7, decimal_places=2)
    date = fields.DateTimeField()
    order_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    departure = fields.DateTimeField()
    pay = fields.BooleanField()

    def __str__(self):
        return str(self.buyer)

# Create your models here.
