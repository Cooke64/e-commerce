from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_to', 'discount', 'active']
    list_filter = ['active']
    search_fields = ['code']