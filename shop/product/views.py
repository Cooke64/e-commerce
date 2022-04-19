from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from cart.forms import CartAddProductForm
from .forms import FeedbackForm, RateForm
from .models import Product, Category, Feedback, Favorite
from .services import get_product_list, save_feedback, save_score


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
    products = get_product_list(request)
    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        products = get_product_list(request, cat_slug=cat_slug,
                                    category=category)
    else:
        category = None
    context = {
        'cats': cats, 'category': category, 'products': products,
    }
    return render(request, 'product/index.html', context)


def product_detail(request, product_slug: str):
    product = Product.available_items.get(slug=product_slug)
    # Увеличиваем количество просмотров товара при каждом обращении
    product.view_count += 1
    product.save()
    feedbacks = Feedback.objects.filter(product=product.pk)
    # Если продукт находится в избранных, то показываем
    # кнопку добавить в избранное
    in_fave = Favorite.objects.filter(
        user=request.user.pk, product=product.pk
    ).exists()
    context = {
        'product': product,
        'form': CartAddProductForm(),
        'feedback_form': FeedbackForm(request.POST or None),
        'feedbacks': feedbacks,
        'in_fave': in_fave,
        'add_score_form': RateForm()
    }
    return render(request, 'product/product_detail.html', context)


@login_required(login_url='login_user')
def add_feedback(request, product_slug):
    """Добавляем отзыв к продукту через пост запрос."""
    product = get_object_or_404(Product, slug=product_slug)
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        save_feedback(request, form, product)
    return redirect('product_detail', product_slug=product_slug)


@login_required
def favorites_items(request):
    """Отображения списка избранных товаров/продуктов."""
    user = request.user
    user_list = user.who_likes_items.values_list('product', flat=True)
    favorite_items = Product.available_items.filter(id__in=user_list)
    context = {'favs': favorite_items}
    return render(request, "product/favorites.html", context)


@login_required
def add_item_in_fav(request, product_slug: str):
    """Добавление товара в категорию избранные через проверку запроса
    к бд на существование у даннго юзера данного товара в избранных.
    """
    fav_item = get_object_or_404(Product, slug=product_slug)
    fav_in_database = (Favorite.objects
                       .filter(user=request.user, product=fav_item).exists()
                       )
    if not fav_in_database:
        Favorite.objects.get_or_create(
            user=request.user, product=fav_item
        )
    return redirect('product_detail', product_slug=product_slug)


@login_required
def stop_being_fav(request, product_slug: str):
    """Удаление товара из избранного."""
    fav_item = get_object_or_404(Product, slug=product_slug)
    fav_in_database = Favorite.objects.filter(
        user=request.user, product=fav_item
    )
    if fav_in_database.exists():
        fav_in_database.delete()
    return redirect('product_detail', product_slug=product_slug)


@login_required
def add_score(request, product_slug: str):
    """Добавления рейтинга/лайков к конкретному товару."""
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        save_score(request, product)
        return redirect('product_detail', product_slug=product_slug)
