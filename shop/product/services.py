from product.forms import RateForm
from product.models import Product


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


def save_feedback(request, form, product):
    """Сохраняем отзыв к товару, отображенному функцией product_detail."""
    try:
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.product = product
        feedback.save()
    except Exception as e:
        raise e


def save_score(request, product):
    try:
        form = RateForm(request.POST)
        score = form.save(commit=False)
        score.user = request.user
        score.product = product
        score.save()
    except Exception as e:
        raise e
