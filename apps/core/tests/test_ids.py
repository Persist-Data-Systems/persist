"""Guard rails for the project's prefixed-id primary keys.

``django-prefix-id`` doesn't itself stop two models from picking the same
prefix, so we check it here across every installed model.
"""

from django.apps import apps
from prefix_id import PrefixIDField


def _prefixed_id_fields():
    for model in apps.get_models():
        field = model._meta.pk
        if isinstance(field, PrefixIDField):
            yield model, field


def test_prefixes_are_unique_across_models():
    seen = {}
    collisions = []
    for model, field in _prefixed_id_fields():
        label = f"{model._meta.app_label}.{model.__name__}"
        if field.prefix in seen:
            collisions.append((field.prefix, seen[field.prefix], label))
        else:
            seen[field.prefix] = label
    assert not collisions, (
        f"Duplicate PrefixIDField prefixes: {[(p, a, b) for p, a, b in collisions]}"
    )


def test_generated_id_round_trips_through_prefix():
    for model, field in _prefixed_id_fields():
        value = field.get_default()
        assert value.startswith(f"{field.prefix}_"), (
            f"{model.__name__}.id default {value!r} missing prefix {field.prefix!r}"
        )
