from django.db import models
from django.contrib.auth.models import User


# КОММЕНТАРИЙ: создавать таблицы реляционной базы данных и практически всем полям разрешать NULL значения — это бессмыслица
# КОММЕНТАРИЙ: если такое поведение базы действительно необходимо по каким-то причинам (для вашего проекта их на самом деле нет), то используйте тогда уж документоориентированную БД


# КОММЕНТАРИЙ: вот здесь вы разрешаете сохранять в таблицу строки с разными первичными ключами (создаваемыми автоматически) и пустыми ячейками во всех прочих столбцах — это не функционально и не имеет смысла с точки зрения хранения данных — более того, это допускает потенциальные многочисленные искажения данных при обновлении и удалении строк этой таблицы
class Customer(models.Model):
    # КОММЕНТАРИЙ: не говоря уже о том, что внешние ключи по определению должны быть NOT NULL
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, )
    # УДАЛИТЬ: поля first_name, last_name и email есть во встроенной модели django.contrib.auth.models.User
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    # ДОБАВИТЬ: а вот поля phone во встроенной модели нет — не факт, что вам нужны номера телефонов, но это хотя бы оправдало создание этой модели

    def __str__(self):
        # ИСПРАВИТЬ здесь и далее: вам необходимо вернуть экземпляр класса str, а не экземпляр CharField
        return self.name


# КОММЕНТАРИЙ: и снова — здесь вы моделируете таблицу так, чтобы в неё можно было записать строку с обязательными первичным ключом и ценой, при всех остальных пустых ячейках — зачем в таблице товаров вам нужны строки с только ценами непонятно чего?
class Product(models.Model):
    objects = None
    name = models.CharField(max_length=200, null=True)
    # ИСПРАВИТЬ: согласно налоговому законодательству (приказ от 14 сентября 2020 г. N ЕД-7-20/662@) для хранения и использования денежных величин в информационно-технических системах необходимо использовать числа с фиксированной, а не плавающей точкой
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        # ИСПРАВИТЬ: не перехватывайте все исключения разом, уточните какое потенциальное исключение может здесь возникнуть
        except:
            url = ''
        return url


class Order(models.Model):
    # КОММЕНТАРИЙ: зачем удалять менеджер объектов? вы не собираетесь выполнять запросы по этим моделям? крайне сомнительно
    objects = None
    # КОММЕНТАРИЙ: такое поведение при удалении покупателя оставит в БД запись о заказе, который выполнен непонятно для кого — в результате получатся те самые "осиротевшие" данные (orphaned data), о которых я говорил в курсе БД
    # КОММЕНТАРИЙ: реляционные БД всеми силами моделируют так, чтобы избежать подобного исхода — а вы на совершенно ровном месте его допускаете
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # КОММЕНТАРИЙ: только два состояния у заказов: не выполнен и выполнен? покупатель нынче избалован продвинутыми сервисами, так что вы рискуете я бы сказал
    complete = models.BooleanField(default=False, null=True, blank=False)
    # КОММЕНТАРИЙ: это разве не должен быть внешний ключ на ещё одну таблицу с подробной информацией о статусе и идентификаторах платежа?
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        # ИСПРАВИТЬ: метод all() должен быть вызван
        orderitems = self.orderitem_set.all
        # КОММЕНТАРИЙ: сейчас вы пытаетесь итерироваться по объекту метода
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        # ИСПОЛЬЗОВАТЬ: не нужно создавать список, достаточно генераторного выражения
        total = sum(item.get_total for item in orderitems)
        return total

    @property
    def get_cart_items(self):
        # ИСПОЛЬЗОВАТЬ: в данном случае однострочник даже читается легче
        return sum(item.quantity for item in self.orderitem_set.all())


class OrderItem(models.Model):
    objects = None
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    # ИСПРАВИТЬ: если товар добавлен в корзину/заказ, то наверное уж его количество не ноль по умолчанию, а один
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    # ДОБАВИТЬ: неплохо было бы с самого начала предусмотреть поле для скидок, например

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    # КОММЕНТАРИЙ: покажите мне почтовый индекс на двести символов, очень любопытно взглянуть
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # ИСПРАВИТЬ: добавьте город что ли — а то получится ещё одна "3-я улица Строителей, дом 25"
        return self.address

