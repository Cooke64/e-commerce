from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from product.models import Product
from .forms import ProductForm
from django.http import JsonResponse


class ProductView(TemplateView):
    template_name = 'staff/all_products.html'


def get_json_response(*args, **kwargs):
    visibility = 3
    upper = kwargs.get('product_pk')
    lower = upper - visibility
    products = list(Product.objects.values()[lower:upper])
    max_size = len(Product.objects.all())
    size = True if upper >= max_size else False
    return JsonResponse({'data': products, 'max': size}, safe=False)


def product_add(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    data = {}
    if request.is_ajax() and form.is_valid():
        form.save()
        data['name'] = form.cleaned_data.get('name')
        data['status'] = 'ok'
        return JsonResponse(data)
    context = {'form': form}
    return render(request, 'staff/staff_page.html', context)


def edit_product(request, product_slug):
    product = Product.available_items.get(slug=product_slug)
    form = ProductForm(
        request.POST or None, files=request.FILES or None, instance=product
    )
    data = {}
    if form.is_valid():
        form.save()
        data['name'] = form.cleaned_data.get('name')
        data['status'] = 'ok'
        return JsonResponse(data)
    context = {'form': form, 'is_edit': True}
    return render(request, 'staff/staff_page.html', context)
