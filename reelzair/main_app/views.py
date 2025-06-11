from django.shortcuts import render, redirect
from .models import Cart, CartItem, Order
from django.utils import timezone
from decimal import Decimal

def get_or_create_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            return Cart.objects.get(id=cart_id, is_checked_out=False)
        except Cart.DoesNotExist:
            pass
    cart = Cart.objects.create()
    request.session['cart_id'] = cart.id
    return cart

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def print_label(request):
    return render(request, 'print_label.html')

def cart(request):
    try:
        cart = get_or_create_cart(request)
        items = cart.items.select_related('product')  

        total = sum(item.product.price * item.quantity for item in items)
    except Cart.DoesNotExist:
        cart = None
        items = []
        total = Decimal('0.00')

    return render(request, 'cart.html', {'cart': items, 'total': total})

def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        shipping_method = request.POST.get('shipping_method')

        shipping_costs = {
            'standard': Decimal('4.99'),
            'express': Decimal('14.99'),
            'eco': Decimal('2.99'),
        }

        try:
            cart = get_or_create_cart(request)
            cart.contact_name = name
            cart.contact_email = email
            cart.contact_phone = phone
            cart.is_checked_out = True
            cart.save()

            items = cart.items.select_related('product')
            total = sum(item.product.price * item.quantity for item in items)
            shipping_price = shipping_costs.get(shipping_method, Decimal('0.00'))
            full_total = total + shipping_price

            order = Order.objects.create(
                cart=cart,
                total_price=full_total,
                paid=True
            )

            request.session['order_id'] = order.id

            return redirect('checkout_success')

        except Cart.DoesNotExist:
            pass  

    return render(request, 'checkout.html', {
        'total': Decimal('0.00'),
        'shipping_price': Decimal('0.00')
    })

def checkout_success(request):
    order_id = request.session.get('order_id')
    order = None

    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            pass

    return render(request, 'checkout_success.html', {'order': order})