from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from cart.forms import CartAddProductForm
from coupons.forms import CouponForm
from .forms import FeedbackForm
from .models import Product, Category, Feedback, Favorite


class SearchResultsView(ListView):
    model = Product
    template_name = 'product/search_result.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
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


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, )
    feedbacks = Feedback.objects.filter(product=product.pk)
    in_fave = Favorite.objects.filter(
        user=request.user.pk,
        product=product.pk
    ).exists()
    feedback_form = FeedbackForm(request.POST or None)
    coupon_apply_form = CouponForm()
    form = CartAddProductForm()
    context = {
        'product': product,
        'form': form,
        'feedback_form': feedback_form,
        'feedbacks': feedbacks,
        'coupon_apply_form': coupon_apply_form,
        'in_fave': in_fave
    }
    return render(request, 'product/product_detail.html', context)


@login_required(login_url='login_user')
def add_feedback(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.product = product
        feedback.save()
    return redirect('product_detail', product_slug=product_slug)


@login_required
def favorites_items(request):
    user = request.user
    user_list = user.who_likes_items.values_list('product', flat=True)
    favs = Product.objects.select_related('category').filter(id__in=user_list)
    context = {'favs': favs}
    return render(request,
                  "product/favorites.html",
                  context
                  )


@login_required
def add_item_in_fav(request, product_slug):
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
def stop_being_fav(request, product_slug):
    fav_item = get_object_or_404(Product, slug=product_slug)
    fav_in_bd = Favorite.objects.filter(user=request.user, product=fav_item)
    if fav_in_bd.exists():
        fav_in_bd.delete()
    return redirect('product_detail', product_slug=product_slug)
