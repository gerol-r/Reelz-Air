from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, Order, Product

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

def product(request):
    return render(request, 'product.html')

def print_label(request):
    return render(request, 'print_label.html')

def cart(request):
    try:
        cart = get_or_create_cart(request)
        items = cart.items.select_related('product')  

        total = cart.total_price()
    except Cart.DoesNotExist:
        cart = None
        items = []
        total = Decimal('0.00')

    return render(request, 'cart.html', {'items': items, 'total': total})

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
            total = cart.total_price()
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

class CartItemUpdateView(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs['pk']
        action = request.POST.get('action')


        item = get_object_or_404(CartItem, pk=item_id)
        cart = get_or_create_cart(request)

        if item.cart != cart:
            return JsonResponse({ 'error': 'Unauthorized'}, status=403)


        if action == 'decrease' and item.quantity > 1:
            item.quantity -= 1
        elif action == 'increase':
            item.quantity += 1

        item.save()
        item_total = float(item.item_total())
        cart_total = float(item.cart.total_price())
        return JsonResponse({'quantity': item.quantity, 'item_total': item_total, 'cart_total': cart_total})


class CartItemDeleteView(View):
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(CartItem, pk=kwargs['pk'])
        cart = get_or_create_cart(request)

        if item.cart != cart:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        item.delete()
        return JsonResponse({'deleted': True})
    
def confirmation(request):
    return render(request, 'confirmation.html')

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        try:
            # Get or create cart
            cart_id = request.session.get('cart_id')
            if not cart_id:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
            else:
                cart = Cart.objects.get(id=cart_id)
            
            # Get first product (assuming it's ReelzAir)
            product = Product.objects.first()
            if not product:
                return JsonResponse({
                    'success': False, 
                    'error': 'Product not found'
                }, status=404)
            
            # Create cart item with product
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1
            )
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            print(f"Error adding to cart: {str(e)}")
            return JsonResponse({
                'success': False, 
                'error': str(e)
            }, status=500)
            
    return JsonResponse({
        'success': False, 
        'error': 'Invalid request method'
    }, status=400)