from django.shortcuts import get_object_or_404

from product.models import Product


def get_detail_queryset(model, slug):
    """Функция получает объект с переданной в функцией моделью и slug"""
    queryset = get_object_or_404(model, slug=slug)
    return queryset


def get_product_list(request, cat_slug=None, category=None):
    products = (Product.objects.
                select_related('category')
                .filter(available=True)
                )
    if cat_slug:
        products = (Product.objects
                    .select_related('category')
                    .filter(category=category)
                    )

    if "all_items" in request.GET:
        # Сортировка всех доступных продуктов
        products = (Product.objects.
                    select_related('category')
                    .filter(available=True)
                    )
    elif "with_feeds" in request.GET:
        # Выбирает товары только с отзывами
        products = (Product.objects
                    .filter(feedbacks__isnull=False)
                    .distinct())
    elif 'max_price' in request.GET:
        # Сортирует по максимальной цене
        products = (Product.objects
                    .order_by('-price')
                    .select_related('category'))
    elif 'min_price' in request.GET:
        # Сортирует по минимальной цене
        products = (Product.objects
                    .order_by('price')
                    .select_related('category'))
    return products


