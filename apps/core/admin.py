from django.contrib import admin

from .models import Address, Organization, Program


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "abbreviation", "institution", "start_year", "is_active")
    list_filter = ("is_active", "institution")
    search_fields = ("name", "abbreviation")
    autocomplete_fields = ("lead", "institution")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("__str__", "city", "region", "country")
    list_filter = ("country",)
    search_fields = ("line_1", "city", "region", "postal_code")


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "abbreviation", "organization_type", "ror_id")
    list_filter = ("organization_type",)
    search_fields = ("name", "abbreviation", "ror_id")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("address",)
