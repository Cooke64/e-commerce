from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views.decorators.http import require_POST


from .models import Coupon
from cart.forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            request.session['coupon_id'] = coupon.id
        except ObjectDoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart_detail')