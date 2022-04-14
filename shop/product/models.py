from customer.models import User
from django.db import models
from django.db.models import Avg

from django.urls import reverse


COLOR_CHOICES = (
    ('Желтый', 'Желтый'),
    ('Красный', 'Красный'),
    ('Синий', 'Синий'),
    ('Черный', 'Черный'),
    ('Золотой', 'Золотой'),
                 )

SIZE_CHOICES = (
    (1, 'XS'),
    (2, 'S'),
    (3, 'M'),
    (4, 'L'),
    (5, 'XL'),
                )

RATE_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
]


class Product(models.Model):
    """
    Модель товары в наличии.
    """
    name = models.CharField('Название', max_length=250)
    color = models.CharField(
        'Цвет', max_length=250, blank=True, choices=COLOR_CHOICES
    )
    size = models.CharField(
        'Размер', max_length=250, blank=True, choices=SIZE_CHOICES
    )
    price = models.DecimalField(
        'Цена', max_digits=10, decimal_places=2
    )
    year = models.CharField(
        'Год выпуска', max_length=250, blank=True, null=True)
    slug = models.SlugField(
        'Ссылка', max_length=100, unique=True)
    description = models.TextField(
        'Описание', null=True, blank=True,
    )
    create_date = models.DateTimeField(
        'Дата', auto_now_add=True)
    images = models.ImageField(
        'Цвет', upload_to='products_img/', blank=True, null=True)
    brand = models.ForeignKey(
        'Brand',
        on_delete=models.CASCADE, related_name='products',
        verbose_name='Брэнд', null=True, blank=True,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE, related_name='products',
        verbose_name='Категория', null=True, blank=True,
    )
    available = models.BooleanField(default=True)
    shop = models.ManyToManyField(
        'Store', related_name='product_item',
        verbose_name='Магазины', null=True, blank=True,
    )
    like = models.ManyToManyField('Likes', related_name="products", blank=True, null=True)
    view_count = models.IntegerField("Количество просмотров товара", default=0)

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})

    def get_average_likes(self):
        product = Product.objects.get(name=self)
        avg_likes = product.likes.aggregate(result=Avg('score'))
        total = 0
        if avg_likes["result"] is not None:
            total = float(avg_likes["result"])
        return total


class Likes(models.Model):
    """Отметки лайков конкретного пользователя."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='likes')
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(choices=RATE_CHOICES, default=1)


class Category(models.Model):
    """Категория товара."""
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
    """Бренд конкретного товара."""
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField('Ссылка', max_length=250, unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Store(models.Model):
    """Магазины, в которых имеется в наличии товар."""
    name = models.CharField('Название', max_length=30)
    address = models.CharField('Адрес', max_length=30, null=True, blank=True)
    contact = models.IntegerField('Контакты', null=True, blank=True)
    picture = models.ImageField('Изображение', upload_to='products_img/',
                                null=True, blank=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'store/{self.name}'


class Feedback(models.Model):
    """Отзыв покупателя на товар."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='feedbacks'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='feedbacks')
    text = models.TextField()
    score = models.IntegerField(choices=RATE_CHOICES, default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:50]


class Favorite(models.Model):
    """Избранные товары пользователя."""
    user = models.ForeignKey(
        User, related_name='who_likes_items', on_delete=models.CASCADE, verbose_name='Покупатель',
    )
    product = models.ForeignKey(
        Product, related_name='favourites', on_delete=models.CASCADE, verbose_name='Избранный товар',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [models.UniqueConstraint(
            fields=['user', 'product', ],
            name='unique_favourites')
        ]
