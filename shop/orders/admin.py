from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer',  'address',  'has_paid', 'created',]
    list_filter = ['has_paid', 'created']
    inlines = [OrderItemInline]
