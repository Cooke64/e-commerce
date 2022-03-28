from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,
                                on_delete=models.CASCADE)
    status = models.CharField(
        'Статус',
        max_length=250,
        default=0
    )
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

    def __str__(self):
        return str(self.user)

