from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from coupons.models import Coupon


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(
        'Email', max_length=255, unique=True,
    )
    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField('Когда зарегистрировался', auto_now_add=True)
    # Код для подтверждения профиля через отправку сообщения на емейл
    code = models.CharField('Код подтверждения', max_length=50, blank=True, null=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

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


class Customer(models.Model):
    """Модель покупателя с персональными данными."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    second_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, null=True, blank=True,)
    address = models.TextField('Адрес', null=True, blank=True,)
    delivery_info = models.TextField('Доставка', null=True, blank=True,)
    spent_money = models.IntegerField('Потрачено денег', default=0)
    last_buy = models.DateField('Последний раз купил', null=True, blank=True)
    promocode = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True,)

    def __str__(self):
        return self.first_name

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

        last_buy_was = Order.objects.filter(user=self.user).last()
        if last_buy_was:
            self.last_buy = last_buy_was.created
        else:
            self.last_buy = None
        super().save(*args, **kwargs)
