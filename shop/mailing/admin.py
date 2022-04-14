from django.contrib import admin

from .models import Mailing


@admin.register(Mailing)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("user", "confirm")
