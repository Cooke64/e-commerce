from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Avg
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from cart.forms import CartAddProductForm
from .forms import FeedbackForm, RateForm
from .models import Product, Category, Feedback, Favorite


class SearchResultsView(ListView):
    model = Product
    template_name = 'product/search_result.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Передаем в шаблон параметры get запроса."""
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        """Получаем список товаров, соответствую их запросу по имени или
        описанию.
        """
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        return object_list


def product_list(request, cat_slug=None):
    cats = Category.objects.all()
    products = (Product.objects.
                select_related('category')
                .filter(available=True)
                )
    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        products = (Product.objects
                    .select_related('category')
                    .filter(category=category)
                    )
    else:
        category = None
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
    context = {
        'cats': cats,
        'category': category,
        'products': products,
    }
    return render(request, 'product/index.html', context)


def product_detail(request, product_slug: str):
    user = request.user
    product = (Product.objects
               .select_related('category',)
               .get(slug=product_slug)
               )
    # Увеличиваем количество просмотров товара при каждом обращении
    product.view_count += 1
    product.save()
    feedbacks = Feedback.objects.filter(product=product.pk)
    # Если продукт находится в избранных, то показываем
    # кнопку добавить в избранное
    in_fave = Favorite.objects.filter(
        user=user.pk,
        product=product.pk
    ).exists()
    feedback_form = FeedbackForm(request.POST or None)
    add_score_form = RateForm()
    form = CartAddProductForm()
    context = {
        'product': product,
        'form': form,
        'feedback_form': feedback_form,
        'feedbacks': feedbacks,
        'in_fave': in_fave,
        'add_score_form': add_score_form
    }
    return render(request, 'product/product_detail.html', context)


@login_required(login_url='login_user')
def add_feedback(request, product_slug):
    """Добавляем отзыв к продукту через пост запрос."""
    product = get_object_or_404(Product, slug=product_slug)
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        try:
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.product = product
            feedback.save()
        except Exception as e:
            raise e
    return redirect('product_detail', product_slug=product_slug)


@login_required
def favorites_items(request):
    """Отображения списка избранных товаров/продуктов."""
    user = request.user
    user_list = user.who_likes_items.values_list('product', flat=True)
    favs = Product.objects.select_related('category').filter(id__in=user_list)
    context = {'favs': favs}
    return render(request, "product/favorites.html", context)


@login_required
def add_item_in_fav(request, product_slug: str):
    """Добавление товара в категорию избранные через проверку запроса
    к бд на существование у даннго юзера данного товара в избранных.
    """
    fav_item = get_object_or_404(Product, slug=product_slug)
    is_exist = (Favorite.objects
                .filter(user=request.user, product=fav_item)
                .exists())
    if not is_exist:
        Favorite.objects.get_or_create(
            user=request.user,
            product=fav_item
        )
    return redirect('product_detail', product_slug=product_slug)


@login_required
def stop_being_fav(request, product_slug: str):
    """Удаление товара из избранного."""
    fav_item = get_object_or_404(Product, slug=product_slug)
    fav_in_bd = Favorite.objects.filter(user=request.user, product=fav_item)
    if fav_in_bd.exists():
        fav_in_bd.delete()
    return redirect('product_detail', product_slug=product_slug)


@login_required
def add_score(request, product_slug: str):
    """Добавления рейтинга/лайков к конкретному товару."""
    product = Product.objects.get(slug=product_slug)
    if request.method == 'POST':
        try:
            form = RateForm(request.POST)
            score = form.save(commit=False)
            score.user = request.user
            score.product = product
            score.save()
        except Exception as e:
            raise e
        return redirect('product_detail', product_slug=product_slug)
