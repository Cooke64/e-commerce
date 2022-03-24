from django.db import models

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

COLOR_CHOICES = (('желтый', 'желтый'),
                ('не желтый', 'не желтый'),
                )
SIZE_CHOICES = (('l', 'L'),
               ('XS', 'XS'),
               )


class Product(models.Model):
    name = models.CharField(max_length=250)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    color = models.CharField(max_length=250, blank=True, null=True,
                             choices=COLOR_CHOICES)
    size = models.CharField(max_length=250, blank=True, null=True,
                            choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='products_img/', blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    store = models.ForeignKey(
        'Store', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Brand(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    contact = models.IntegerField(null=True)
    products = models.ManyToManyField(Product, blank=True)
    picture = models.ImageField(upload_to='products_img/', null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'store/{self.name}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
