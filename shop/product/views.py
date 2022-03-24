from django.shortcuts import render, get_object_or_404, redirect

from cart.forms import CartAddProductForm
from coupons.forms import CouponForm
from .forms import CommentForm
from .models import Product, Category, Brand, Comment


def index(request, cat_slug=None):
    cats = Category.objects.all()
    products = Product.objects.filter(available=True)
    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        products = products.filter(category=category)
    else:
        category = None
    context = {
        'cats': cats,
        'category': category,
        'products': products
    }
    return render(request, 'product/index.html', context)


def brand_page(request, brand_slug=None):
    brands = Brand.objects.all()
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        products = Product.objects.filter(brand=brand)
    else:
        brand = None
        products = None
    context = {
        'brands': brands,
        'brand': brand,
        'products': products,
    }
    return render(request, 'product/brand_list.html', context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug,)
    comments = Comment.objects.filter(product=product.pk)
    comment_form = CommentForm(request.POST or None)
    coupon_apply_form = CouponForm()
    form = CartAddProductForm()
    context = {
        'product': product,
        'form': form,
        'comment_form': comment_form,
        'comments': comments,
        'coupon_apply_form': coupon_apply_form,
    }
    return render(request, 'product/product_detail.html', context)


def add_comment(request, product_slug):
    post = get_object_or_404(Product, slug=product_slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('product_detail', slug=product_slug)



