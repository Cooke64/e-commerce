# Generated by Django 3.2.12 on 2022-04-25 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Ссылка')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название')),
                ('address', models.CharField(blank=True, max_length=30, null=True, verbose_name='Адрес')),
                ('contact', models.IntegerField(blank=True, null=True, verbose_name='Контакты')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='products_img/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('color', models.CharField(blank=True, choices=[('Желтый', 'Желтый'), ('Красный', 'Красный'), ('Синий', 'Синий'), ('Черный', 'Черный'), ('Золотой', 'Золотой')], max_length=250, verbose_name='Цвет')),
                ('size', models.CharField(blank=True, choices=[(1, 'XS'), (2, 'S'), (3, 'M'), (4, 'L'), (5, 'XL')], max_length=250, verbose_name='Размер')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('year', models.CharField(blank=True, max_length=250, null=True, verbose_name='Год выпуска')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Ссылка')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('images', models.ImageField(blank=True, null=True, upload_to='products_img/', verbose_name='Цвет')),
                ('available', models.BooleanField(default=True)),
                ('view_count', models.IntegerField(default=0, verbose_name='Количество просмотров товара')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.brand', verbose_name='Брэнд')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category', verbose_name='Категория')),
                ('like', models.ManyToManyField(blank=True, null=True, related_name='products', to='product.Likes')),
                ('shop', models.ManyToManyField(blank=True, null=True, related_name='product_item', to='product.Store', verbose_name='Магазины')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='likes',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='product.product'),
        ),
        migrations.AddField(
            model_name='likes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('score', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='product.product', verbose_name='Избранный товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_likes_items', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_favourites'),
        ),
    ]
