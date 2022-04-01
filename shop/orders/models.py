from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django.db import models

from product.models import Product

User = get_user_model()

delivery_choice = (('Post', 'Post'),
                   ('No post', 'No post'),
                   )


class Order(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='orders')
    address = models.CharField(max_length=150)
    comment = models.CharField(max_length=30)
    delivery = models.CharField(max_length=250, blank=True, null=True,
                                choices=delivery_choice)
    created = models.DateTimeField(auto_now_add=True)
    has_paid = models.BooleanField(default=False)
    will_be_delivered = models.DateTimeField()

    class Meta:
        ordering = ('-created',)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def save(self, *args, **kwargs):
        self.will_be_delivered = datetime.now() + timedelta(3)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return (self.price * self.quantity)

    def __str__(self):
        return self.product.name


