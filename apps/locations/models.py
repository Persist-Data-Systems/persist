"""Sites, fields, and plot geometry.

Minimal stub for now — just enough of a `Location` for `germplasm` (and later
`trials` / `phenotyping`) to FK against. Full spatial modelling (PostGIS
geometry, plot polygons, weather stations) comes when this app is designed;
that work goes behind ``settings.USE_GIS``.
"""

from django.db import models
from prefix_id import PrefixIDField

from apps.core.models import BaseModel


class Location(BaseModel):
    id = PrefixIDField(prefix="loc", primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    code = models.CharField(max_length=50, blank=True)
    location_type = models.CharField(
        max_length=30,
        blank=True,
        help_text="e.g. site, field, block, greenhouse, nursery, collection point",
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    elevation_m = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=3, blank=True, help_text="ISO 3166-1 alpha-3")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
