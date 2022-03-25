from django.contrib import admin
from .models import Product, Category, Brand, Store


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'brand',
        'price',
        'create_date',
        'category',
    )
    search_fields = ('name', 'brand', 'price')
    list_editable = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
