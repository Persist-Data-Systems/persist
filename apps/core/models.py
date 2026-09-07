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
from django.db import models
from prefix_id import PrefixIDField


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
    institution = models.CharField(max_length=200, blank=True)
    start_year = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.abbreviation or self.name
