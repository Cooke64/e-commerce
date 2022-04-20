from typing import Union, Any

from django.shortcuts import get_object_or_404

from product.forms import RateForm
from product.models import Product, Feedback, Favorite


def get_product_list(request, cat_slug=None, category=None):
    """Функция возвращает различные query sets в зависимости
     от запроса, переданная аргументов get-запроса."""
    products = Product.available_items.all()
    if cat_slug:
        products = Product.available_items.filter(category=category)
    if "all_items" in request.GET or None in request.GET:
        # Сортировка всех доступных продуктов
        products = products
    elif "with_feeds" in request.GET:
        # Выбирает товары только с отзывами
        products = (Product.available_items
                    .filter(feedbacks__isnull=False)
                    .distinct())
    elif 'max_price' in request.GET:
        # Сортирует по максимальной цене
        products = Product.available_items.order_by('-price')
    elif 'min_price' in request.GET:
        # Сортирует по минимальной цене
        products = Product.available_items.order_by('price')
    return products


def save_feedback(request, form, product_slug):
    """Сохраняем отзыв к товару, отображенному функцией product_detail."""
    product = get_object_or_404(Product, slug=product_slug)
    try:
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.product = product
        feedback.save()
    except Exception as e:
        raise e


def save_score(request, product_slug):
    """Простановка рейтинга к товару."""
    product = get_object_or_404(Product, slug=product_slug)
    try:
        form = RateForm(request.POST)
        score = form.save(commit=False)
        score.user = request.user
        score.product = product
        score.save()
    except Exception as e:
        raise e


def get_product_and_add_views(product_slug):
    """Получаем продукт, при переходе на текущую страничку увеличиваем количество просмотров товара."""
    product = Product.available_items.get(slug=product_slug)
    # Увеличиваем количество просмотров товара при каждом обращении
    product.view_count += 1
    product.save()
    return product


def get_feedback_and_fav(request, product: Any) -> Union[dict]:
    """Получаем все отзывы на товар, а так же отображаем кнопку добавить в избранное,
    если товар не находится у пользователя в избранном.
    """
    feedbacks = Feedback.objects.filter(product=product.pk)
    # Если продукт находится в избранных, то показываем
    # кнопку добавить в избранное
    in_fave = Favorite.objects.filter(
        user=request.user.pk, product=product.pk
    ).exists()
    return {'feedbacks': feedbacks, 'in_fave': in_fave}


def check_product_in_fave_list(request, product_slug: str) -> None:
    """Получаем продукт, проверяем наличием данного продукта
    в избранных у пользователя. Если есть, то удаляем.
    """
    fav_item = get_object_or_404(Product, slug=product_slug)
    fav_in_database = (Favorite.objects
                       .filter(user=request.user, product=fav_item)
                       )
    if fav_in_database.exists():
        fav_in_database.delete()
    else:
        Favorite.objects.get_or_create(
            user=request.user, product=fav_item
        )


def get_fav_items(request):
    """Получаем список избранных товаров пользователя."""
    user = request.user
    user_list = user.who_likes_items.values_list('product', flat=True)
    return Product.available_items.filter(id__in=user_list)
