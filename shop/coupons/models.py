from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(
        default=5, validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
