from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from customer.managers import CustomUserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField('Email', max_length=255, unique=True,)
    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField('Когда зарегистрировался', auto_now_add=True)
    # Код для подтверждения профиля через отправку сообщения на емейл
    code = models.CharField('Код подтверждения', max_length=50, blank=True, null=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class UserQueryManager(models.Manager):
    def get_subscribed(self):
        return super(UserQueryManager, self).select_related('users').get_queryset().filter(subscribed=True)


class Customer(models.Model):
    """Модель покупателя с персональными данными."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    second_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, null=True, blank=True,)
    address = models.TextField('Адрес', null=True, blank=True,)
    delivery_info = models.TextField('Доставка', null=True, blank=True,)
    spent_money = models.IntegerField('Потрачено денег', default=0)
    last_buy = models.DateField('Последний раз купил', null=True, blank=True)
    subscribed = models.BooleanField('Подписка на рассылку', default=True)

    subscribed_user = UserQueryManager()
    objects = models.Manager()

    def __str__(self):
        return f'{self.user}'

    def get_discount(self):
        """Определяет размер скидки в зависимости от потраченных денег покупателем"""
        if self.spent_money < 10:
            discount = 5
        elif self.spent_money < 20:
            discount = 10
        else:
            discount = 15
        return discount

    def save(self, *args, **kwargs):
        """Определяет дату последней покупки и присваивает
        дату последнего заказа текущего покупателя."""
        from orders.models import Order

        last_buy_was = Order.objects.filter(customer_id=self.user).last()
        if last_buy_was:
            self.last_buy = last_buy_was.created
        else:
            self.last_buy = None
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    instance.customer.save()

