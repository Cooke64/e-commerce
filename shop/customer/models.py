from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,
                                on_delete=models.CASCADE)

    phone = models.IntegerField(
        null=True,
        blank=True,)
    address = models.TextField(
        'Адрес',
        null=True,
        blank=True,
    )
    delivery_info = models.TextField(
        'Доставка',
        null=True,
        blank=True,
    )
    spent_money = models.IntegerField(
        'Потрачено денег',
        default=0)

    def __str__(self):
        return str(self.user)

    def get_discount(self):
        if self.spent_money < 10:
            discount = 5
        elif self.spent_money < 20:
            discount = 10
        else:
            discount = 15
        return discount
