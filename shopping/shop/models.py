from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields


class Category(models.Model):
    name = fields.CharField(max_length=50)
    description = fields.TextField()
    image = models.ImageField(null=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = fields.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = fields.DecimalField(max_digits=7, decimal_places=2)
    availability = fields.PositiveSmallIntegerField()
    image = models.ImageField(null=True)
    discount = fields.SmallIntegerField(default=0)
    baskets = models.ManyToManyField(
        'Basket',
        through='BasketProduct'
    )

    class Meta:
        db_table = 'products'

    def __str__(self):
        return str(self.name)


class Basket(models.Model):
    total = fields.DecimalField(max_digits=7, decimal_places=2)
    discount = fields.PositiveSmallIntegerField(null=True)

    class Meta:
        db_table = 'baskets'

    def __str__(self):
        return str(self.total)


class BasketProduct(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = fields.PositiveSmallIntegerField()

    class Meta:
        db_table = 'products_baskets'


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    discount = fields.PositiveSmallIntegerField(null=True)
    phone = fields.CharField(max_length=15, null=True)

    class Meta:
        db_table = 'clients'

    def __str__(self):
        return f'{self.user.username}'


class Delivery(models.Model):
     method = fields.CharField(max_length=20)

     class Meta:
         db_table = 'deliveries'

     def __str__(self):
         return str(self.method)


class Address(models.Model):
    country = fields.CharField(max_length=50)
    city = fields.CharField(max_length=30)
    street = fields.CharField(max_length=40)
    house = fields.CharField(max_length=5)
    building = fields.PositiveSmallIntegerField(null=True)
    apartment = fields.PositiveSmallIntegerField()
    index = fields.CharField(max_length=6)

    class Meta:
        db_table = 'addresses'

    def __str__(self):
        ins = f'/{self.building}' if str(self.building) else ''
        return f'{self.index}, {self.city}, {self.street} {self.house}{ins}, {self.apartment}'


class Status(models.Model):
    status = fields.CharField(max_length=45)

    class Meta:
        db_table = 'statuses'

    def __str__(self):
        return str(self.status)


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    basket = models.OneToOneField(Basket, on_delete=models.CASCADE)
    total = fields.DecimalField(max_digits=7, decimal_places=2)
    creation_date = fields.DateTimeField()
    order_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    departure_date = fields.DateTimeField()
    payed = fields.BooleanField()
    staff = models.ManyToManyField(User)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"({self.creation_date}) {self.client}"

