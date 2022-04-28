from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from customer.services import generate_code
from .models import Coupon
from cart.forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    """Применяем промокод к заказу. Берем купон по его коду, если существует у данного купона
    пользователь, к которому он привязан, после применения удаляем такой купон.
    """
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.select_related('user').get(code__iexact=code, active=True)
            request.session['coupon_id'] = coupon.id
            if coupon.user.exits():
                coupon.delete()
        except ObjectDoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart_detail')


def generate_promocode():
    """Создает промокод для скидки."""
    code = generate_code()
    try:
        Coupon.objects.create(code=code,)
        return code
    except ObjectDoesNotExist as e:
        raise e
