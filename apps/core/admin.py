from django.contrib import admin

from .models import Program


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "abbreviation", "institution", "start_year", "is_active")
    list_filter = ("is_active", "institution")
    search_fields = ("name", "abbreviation")
