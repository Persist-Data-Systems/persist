"""Plant-material storage, stock items, and stock transactions.

Storage is a hierarchy: an Organization owns StorageSites, each holding a tree
of StorageLocations (freezer room > freezer > shelf > box). InventoryItems sit
in a StorageLocation and every quantity change is logged as an
InventoryTransaction.

Germplasm still has TODOs pointing at ``inventory.SeedLot`` and
``inventory.PropagationBatch``; those are not modelled yet.
"""

from django.conf import settings
from django.db import models
from prefix_id import PrefixIDField

from apps.core.models import BaseModel

from .enums import MaterialType


class StorageSite(BaseModel):
    """A site (building, facility) that contains storage locations."""

    id = PrefixIDField(prefix="stsite", primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(
        "core.Organization",
        on_delete=models.CASCADE,
        related_name="storage_sites",
    )
    location = models.ForeignKey(
        "locations.Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="storage_sites",
    )
    address = models.ForeignKey(
        "core.Address",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="storage_sites",
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"], name="uniq_storage_site_per_org"
            )
        ]

    def __str__(self):
        return self.name


class StorageLocation(BaseModel):
    """A nestable storage unit: greenhouse, growth chamber, freezer, shelf, box..."""

    id = PrefixIDField(prefix="stloc", primary_key=True)
    site = models.ForeignKey(
        StorageSite, on_delete=models.CASCADE, related_name="locations"
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    name = models.CharField(max_length=255)
    location_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. greenhouse, growth chamber, freezer, shelf, box",
    )
    position = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["site", "name"]

    def __str__(self):
        if self.parent_id:
            return f"{self.parent} > {self.name}"
        return f"{self.site} > {self.name}"


class InventoryItem(BaseModel):
    """A quantity of one kind of material from one Germplasm, in one place."""

    id = PrefixIDField(prefix="invt", primary_key=True)
    germplasm = models.ForeignKey(
        "germplasm.Germplasm",
        on_delete=models.PROTECT,
        related_name="inventory",
    )
    material_type = models.CharField(max_length=20, choices=MaterialType.choices)
    location = models.ForeignKey(
        StorageLocation, on_delete=models.PROTECT, related_name="items"
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=20)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["germplasm", "material_type"]

    def __str__(self):
        return (
            f"{self.germplasm} — {self.get_material_type_display()} "
            f"({self.quantity} {self.unit})"
        )


class InventoryTransaction(BaseModel):
    """A signed quantity change against an InventoryItem."""

    id = PrefixIDField(prefix="invtx", primary_key=True)
    item = models.ForeignKey(
        InventoryItem, on_delete=models.PROTECT, related_name="transactions"
    )
    delta = models.DecimalField(max_digits=10, decimal_places=3)
    reason = models.CharField(max_length=255)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inventory_transactions",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        sign = "+" if self.delta >= 0 else ""
        return f"{self.item} {sign}{self.delta} ({self.reason})"
