from django.urls import path
from . import views # Import views to connect routes to view functions
from .views import CartItemUpdateView, CartItemDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('cart/item/<int:pk>/update/', CartItemUpdateView.as_view(), name='cart_item_update'),
    path('cart/item/<int:pk>/delete/', CartItemDeleteView.as_view(), name='cart_item_delete'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success', views.checkout_success, name='checkout_success'),
    path('printlabel/', views.print_label, name='print_label'),
]
