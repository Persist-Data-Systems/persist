from django.contrib import admin

from .models import InventoryItem, InventoryTransaction, StorageLocation, StorageSite


@admin.register(StorageSite)
class StorageSiteAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "location")
    list_filter = ("organization",)
    search_fields = ("name",)
    autocomplete_fields = ("organization", "location", "address")


@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "site", "location_type", "position")
    list_filter = ("site", "location_type")
    search_fields = ("name",)
    autocomplete_fields = ("site", "parent")


class InventoryTransactionInline(admin.TabularInline):
    model = InventoryTransaction
    extra = 0
    autocomplete_fields = ("performed_by",)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("germplasm", "material_type", "quantity", "unit", "location")
    list_filter = ("material_type",)
    search_fields = ("germplasm__name",)
    autocomplete_fields = ("germplasm", "location")
    inlines = [InventoryTransactionInline]


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ("item", "delta", "reason", "performed_by", "created_at")
    search_fields = ("reason", "item__germplasm__name")
    autocomplete_fields = ("item", "performed_by")
