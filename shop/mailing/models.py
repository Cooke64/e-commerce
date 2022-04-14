from django.db import models

from coupons.models import Coupon
from customer.models import User


class Mailing(models.Model):
    """Рассылка по email."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailing_to')
    text = models.TextField('Текст рекламной рассылки')
    promo_code = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Промокод')
    timestamp = models.DateTimeField('Дата', auto_now_add=True)
    # Данное поле используется для согласия пользователя получать рассылку рекламную
    confirm = models.BooleanField('Согласие на получение', default=True)
