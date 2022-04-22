from decimal import Decimal
from django.conf import settings

from product.models import Product
from coupons.models import Coupon


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.coupon_id = self.session.get('coupon_id')
        if request.user.is_authenticated:
            self.customer = request.user
        else:
            self.customer = None
        self.cart = cart

    def add(self, product, quantity=1,  update_quantity=False, ):
        """Добавляем продукт в корзину."""
        product_slug = str(product.slug)
        if product_slug not in self.cart:
            self.cart[product_slug] = {
                'quantity': 0, 'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_slug]['quantity'] = quantity
        else:
            self.cart[product_slug]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        """Удаляем продукт из корзины."""
        product_slug = str(product.slug)
        if product_slug in self.cart:
            del self.cart[product_slug]
            self.save()

    def __iter__(self):
        """Через цикл проходим по всем товарам корзины."""
        product_slug = self.cart.keys()
        products = Product.objects.filter(slug__in=product_slug)
        for product in products:
            self.cart[str(product.slug)]['product'] = product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self) -> int:
        if self.customer:
            total = self.get_total_price() - (self.get_total_price() / Decimal(self.customer.get_discount()))
        else:
            total = self.get_total_price()
        return total

    def price_with_coupon(self) -> int:
        total = self.get_total_price_after_discount() - self.get_discount()
        return total
