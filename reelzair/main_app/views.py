from django.shortcuts import render, redirect
from .models import Cart, Order
from django.utils import timezone
from decimal import Decimal
# Define the home view function
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cart(request):
    return render(request, 'cart.html')

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

        filtration_quantity = int(request.POST.get('filtration_quantity', 1))
        filter_quantity = int(request.POST.get('filter_quantity', 2))

        cart = Cart.objects.create(
            contact_name=name,
            contact_email=email,
            contact_phone=phone,
            filtration_system_quantity=filtration_quantity,
            filter_replacement_quantity=filter_quantity,
            is_checked_out=True
        )
        

        shipping_price = shipping_costs.get(shipping_method, Decimal('0.00'))
        total = Decimal(cart.total_price())

        order = Order.objects.create(
            cart=cart,
            total_price=total,
            paid=True
        )
        return redirect('checkout_success')
    total = Decimal('0.00')
    shipping_price = Decimal('0.00')
    
    return render(request, 'checkout.html', {'total': total, 'shipping_price': shipping_price})

def checkout_success(request):
    latest_order = Order.objects.latest('id')
    return render(request, 'checkout_success.html', {'order': latest_order})