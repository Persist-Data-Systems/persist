"""Custom user model.

Set as ``AUTH_USER_MODEL = "accounts.User"`` in settings. Swapping the user
model after the first migration is very painful, so keep this in place.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from prefix_id import PrefixIDField


class User(AbstractUser):
    """Project user. Extends Django's ``AbstractUser`` with profile fields."""

    id = PrefixIDField(prefix="usr", primary_key=True)
    bio = models.TextField(blank=True)

    class Meta:
        db_table = "accounts_user"
