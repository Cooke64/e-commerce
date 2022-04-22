from django.shortcuts import render
from .forms import ProductForm
from django.http import JsonResponse


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

