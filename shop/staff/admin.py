from django.contrib import admin

from staff.models import Photo


@admin.register(Photo)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created',
    )
