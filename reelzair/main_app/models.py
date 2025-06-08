from django.db import models
from decimal import Decimal


class Cart(models.Model):
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_checked_out = models.BooleanField(default=False)

    filtration_system_quantity = models.PositiveIntegerField(default=0)
    filter_replacement_quantity = models.PositiveIntegerField(default=0)

    def total_price(self):
        system_price = Decimal('129.99')  
        filter_price = Decimal('11.99')

        return (self.filtration_system_quantity * system_price) + \
               (self.filter_replacement_quantity * filter_price)

    def __str__(self):
        return f"Cart #{self.id} for {self.contact_name}"
    


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - ${self.total_price}"