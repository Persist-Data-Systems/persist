"""Enumerations for the inventory app."""

from django.db import models


class MaterialType(models.TextChoices):
    SEED = "seed", "Seed"
    POLLEN = "pollen", "Pollen"
    TUBER = "tuber", "Tuber"
    RHIZOME = "rhizome", "Rhizome"
    BULB = "bulb", "Bulb"
    CALLUS = "callus", "Callus"
    MEDIA = "media", "Tissue Culture Media"
    TISSUE = "tissue", "Tissue"
    DNA = "dna", "DNA"
    RNA = "rna", "RNA"
    VEG_MATERIAL = "vegetative", "Vegetative Material"
