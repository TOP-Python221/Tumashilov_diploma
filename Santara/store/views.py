import json

from django.http import JsonResponse
from django.shortcuts import render

from .models import *


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        # ИСПРАВИТЬ: метод должен быть вызван
        cart_items = order.get_cart_items
    else:
        items = []
        # ИСПРАВИТЬ здесь и далее: ерунду с ключами
        order = {'get_cart_total': 0, 'def get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_Items']

    products = Product.objects.all()
    context = {'items': items,'products': products, 'cartItems': cart_items}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # КОММЕНТАРИЙ: и как же, интересно, возможен вызов метода get_or_create() если у вас в Order.objects объект None записан?
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'def get_cart_items': 0, 'shipping': False}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'def get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_Items']
    context = {'items':  items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    # КОММЕНТАРИЙ: такой запрос должен быть согласован с диспетчером URL — такую обработку вообще удобнее делать, используя шаблоны диспетчера
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem,created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({'message': 'Item was added'}, safe=False)

