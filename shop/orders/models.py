from datetime import timedelta, datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

from coupons.models import Coupon
from product.models import Product

User = get_user_model()

DELIVERY_CHOICES = (('Post', 'Post'),
                    ('No post', 'No post'),
                    )


class Order(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='orders')
    address = models.CharField(max_length=150)
    comment = models.CharField(max_length=30)
    delivery = models.CharField(
        max_length=250, blank=True, null=True, choices=DELIVERY_CHOICES
    )
    created = models.DateTimeField(auto_now_add=True)
    has_paid = models.BooleanField(default=False)
    will_be_delivered = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(
        Coupon, related_name='orders', on_delete=models.SET_NULL,  null=True, blank=True
    )
    discount = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))

    def save(self, *args, **kwargs):
        """СОхраняем дату доставки."""
        self.will_be_delivered = datetime.now() + timedelta(3)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return self.product.name
