"""Shared abstract base models.

Domain apps should subclass :class:`BaseModel` instead of
``django.db.models.Model`` for the audit timestamps, and declare their own
prefixed-id primary key on top of it::

    from prefix_id import PrefixIDField

    class Widget(BaseModel):
        id = PrefixIDField(prefix="wgt", primary_key=True)

``PrefixIDField`` (from the ``django-prefix-id`` package) stores a real
``prefix_<base62 uuid4>`` string as the primary key, e.g. ``wgt_2t9k4Vw8Xq``.
It's base62 of a random ``uuid4`` — not a ULID/UUIDv7 — so the id carries no
timestamp and reveals nothing about insertion order. Prefixes must be unique
across the whole project; ``apps.core.tests.test_ids`` enforces that.
"""

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from prefix_id import PrefixIDField

from .enums import InstitutionType


class TimeStampedModel(models.Model):
    """Adds self-managed ``created_at`` / ``updated_at`` columns."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel):
    """Default base for domain models: audit timestamps.

    Subclasses must declare their own prefixed-id primary key — see the
    module docstring.
    """

    class Meta:
        abstract = True


class Address(BaseModel):
    """A postal address, shared by organizations (and later sites/buildings)."""

    id = PrefixIDField(prefix="addr", primary_key=True)
    line_1 = models.CharField(
        max_length=255, help_text="Street address, P.O. Box, or c/o"
    )
    line_2 = models.CharField(max_length=255, blank=True)
    line_3 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    region = models.CharField(
        max_length=100, blank=True, help_text="State, province, or region"
    )
    postal_code = models.CharField(
        max_length=20, blank=True, help_text="ZIP or postal code"
    )
    country = models.CharField(max_length=3, help_text="ISO 3166-1 alpha-3")

    class Meta:
        ordering = ["country", "region", "city"]
        verbose_name_plural = "addresses"

    def __str__(self):
        parts = [self.line_1, self.line_2, self.line_3, self.city, self.region]
        parts += [self.postal_code, self.country]
        return ", ".join(p for p in parts if p)


class Organization(BaseModel):
    """A research institution, company, or group that owns programs, storage
    sites, germplasm, trials, etc."""

    id = PrefixIDField(prefix="org", primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=30, blank=True)
    organization_type = models.CharField(max_length=30, choices=InstitutionType.choices)
    address = models.ForeignKey(
        Address,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="organizations",
    )
    ror_id = models.CharField(
        "ROR ID",
        max_length=30,
        null=True,
        blank=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^https://ror\.org/[a-zA-Z0-9]{9}$",
                message="Enter a valid ROR ID in the format https://ror.org/XXXXXXXXX.",
            )
        ],
    )
    logo_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Program(BaseModel):
    """A breeding program / project. Referenced by germplasm, breeding, trials."""

    id = PrefixIDField(prefix="prog", primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    abbreviation = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="led_programs",
    )
    institution = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="programs",
    )
    start_year = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.abbreviation or self.name
