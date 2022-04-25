from django.http import JsonResponse
from django.shortcuts import render

from mailing.forms import ReviewForm


def add_review_to_cite(request):
    form = ReviewForm(request.POST or None)
    data = {}
    if request.is_ajax() and form.is_valid():
        form.save()
        data['message'] = form.cleaned_data.get('text')
        data = {}
        return JsonResponse(data)
    context = {'form': form}
    return render(request, 'staff/review.html', context)
