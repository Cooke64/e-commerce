import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

from cart.forms import CartAddProductForm
from .forms import FeedbackForm, RateForm
from .models import Product, Category, Feedback, Favorite
from .services import get_product_list, save_feedback, save_score, \
    get_product_and_add_views, get_feedback_and_fav, \
    check_product_in_fave_list, get_fav_items


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


def product_list(request, cat_slug=None, category=None):
    """Отображаются все товары по определенному запросу, выбранному пользователем сайта."""
    cats = Category.objects.all()
    products = get_product_list(request)
    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        products = get_product_list(request, cat_slug=cat_slug,
                                    category=category)
    context = {
        'cats': cats, 'category': category, 'products': products,
    }
    return render(request, 'product/index.html', context)


def product_detail(request, product_slug: str):
    """Отображение продукта, с формой для постановки рейтинга, добавлением
    комментария, отображением комментариев и добавлением товара в корзину.
    """
    product = get_product_and_add_views(product_slug)
    query = get_feedback_and_fav(request, product)
    context = {
        'product': product,
        'form': CartAddProductForm(),
        'feedback_form': FeedbackForm(request.POST or None),
        'feedbacks': query.get('feedbacks'),
        'in_fave': query.get('in_fave'),
        'add_score_form': RateForm()
    }
    return render(request, 'product/product_detail.html', context)


@login_required(login_url='login_user')
def add_feedback(request, product_slug):
    """Добавляем отзыв к продукту через пост запрос."""
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        save_feedback(request, form, product_slug)
    return redirect('product_detail', product_slug=product_slug)


@login_required
def favorites_items(request):
    """Отображения списка избранных товаров/продуктов."""
    context = {'favs': get_fav_items(request)}
    return render(request, "product/favorites.html", context)


@login_required
def add_item_in_fav(request, product_slug: str):
    """Добавление товара в категорию избранные."""
    check_product_in_fave_list(request, product_slug)
    return redirect('product_detail', product_slug=product_slug)


@login_required
def stop_being_fav(request, product_slug: str):
    """Удаление товара из избранного."""
    check_product_in_fave_list(request, product_slug)
    return redirect('product_detail', product_slug=product_slug)


@login_required
def add_score(request, product_slug: str):
    """Добавления рейтинга/лайков к конкретному товару."""
    if request.method == 'POST':
        save_score(request, product_slug)
        return redirect('product_detail', product_slug=product_slug)
