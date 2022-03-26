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
    name = models.CharField('Название', max_length=250)
    color = models.CharField(
        'Цвет',
        max_length=250,
        null=True,
        blank=True,
        choices=COLOR_CHOICES
    )
    size = models.CharField(
        'Размер',
        max_length=250,
        null=True,
        blank=True,
        choices=SIZE_CHOICES
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2
    )
    year = models.CharField(
        'Год выпуска', max_length=250, blank=True, null=True)
    slug = models.SlugField(
        'Ссылка', max_length=100, unique=True)
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    create_date = models.DateTimeField(
        'Дата', auto_now_add=True)
    images = models.ImageField(
        'Цвет', upload_to='products_img/', blank=True, null=True)
    brand = models.ForeignKey(
        'Brand',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Брэнд',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    available = models.BooleanField(default=True)
    shop = models.ManyToManyField(
        'Store',
        related_name='product_item',
        verbose_name='Магазины',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


class Category(models.Model):
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField('Ссылка', max_length=250, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Brand(models.Model):
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField('Ссылка', max_length=250, unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField('Название', max_length=30)
    address = models.CharField('Адрес', max_length=30, null=True, blank=True)
    contact = models.IntegerField('Контакты', null=True, blank=True)
    picture = models.ImageField('Изображение', upload_to='products_img/', null=True, blank=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'store/{self.name}'


class Feedback(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='feedbacks'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='feedbacks')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:50]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='customer',
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
    )
    product = models.ForeignKey(
        User,
        related_name='favourites',
        on_delete=models.CASCADE,
        verbose_name='Избранный товар',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [models.UniqueConstraint(
            fields=['user', 'product'],
            name='unique_favourites')
        ]
