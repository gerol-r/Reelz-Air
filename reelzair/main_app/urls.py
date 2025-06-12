from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('product/', views.product, name='product'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('figma/', views.figma, name='figma')
]
