from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from customer.models import Customer, User


@admin.register(Customer)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'phone')
    fieldsets = (
        ('Персональные данные', {'fields': ('first_name', 'second_name', 'phone')}),
        ('Доставка', {'fields': ('address', 'delivery_info', 'spent_money')}),
    )


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['email', 'admin', 'timestamp']
    list_filter = ['admin']
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()
    fieldsets = (
        ('Данные пользователя', {'fields': ('email',)}),
    )
