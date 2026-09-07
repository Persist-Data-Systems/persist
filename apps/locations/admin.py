from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "location_type", "parent", "country")
    list_filter = ("location_type", "country")
    search_fields = ("name", "code")
    autocomplete_fields = ("parent",)
