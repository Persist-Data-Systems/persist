"""Controlled vocabularies for the germplasm app.

Where a term maps to an external standard the code is kept close to it
(MCPD SAMPSTAT for ``BiologicalStatus``, BrAPI-ish germplasm types).
"""

from django.db import models


class MatingSystem(models.TextChoices):
    SELF_POLLINATING = "SELF", "Self-pollinating"
    CROSS_POLLINATING = "CROSS", "Cross-pollinating"
    MIXED = "MIXED", "Mixed mating"
    APOMICTIC = "APOMICT", "Apomictic"
    UNKNOWN = "UNKNOWN", "Unknown"


class PropagationMode(models.TextChoices):
    SEED = "SEED", "Seed"
    CUTTING = "CUTTING", "Cutting"
    CLONAL = "CLONAL", "Clonal"
    UNKNOWN = "UNKNOWN", "Unknown"


class GrowthHabit(models.TextChoices):
    HERBACEOUS = "HERB", "Herbaceous"
    GRAMINOID = "GRAMINOID", "Graminoid"
    SHRUB = "SHRUB", "Shrub"
    TREE = "TREE", "Tree"
    VINE = "VINE", "Vine / liana"
    OTHER = "OTHER", "Other"


class GermplasmType(models.TextChoices):
    WILD_COLLECTION = "WILD_COLLECTION", "Wild collection"
    LANDRACE = "LANDRACE", "Landrace"
    CULTIVAR = "CULTIVAR", "Cultivar / released variety"
    BREEDING_POPULATION = "BREEDING_POPULATION", "Breeding population"
    SYNTHETIC = "SYNTHETIC", "Synthetic"
    FAMILY = "FAMILY", "Family (cross progeny)"
    INBRED_LINE = "INBRED_LINE", "Inbred line"
    GENETIC_STOCK = "GENETIC_STOCK", "Genetic stock"
    NAMED_CLONE = "NAMED_CLONE", "Named clone"
    HYBRID = "HYBRID", "Hybrid"
    UNKNOWN = "UNKNOWN", "Unknown"


class MaterialUse(models.TextChoices):
    SCION = "SCION", "Scion"
    ROOTSTOCK = "ROOTSTOCK", "Rootstock"
    BOTH = "BOTH", "Both"
    NA = "NA", "Not applicable"


class GermplasmStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    OBSOLETE = "OBSOLETE", "Obsolete"
    DISCARDED = "DISCARDED", "Discarded"
    MERGED = "MERGED", "Merged into another record"


class SourceType(models.TextChoices):
    INTERNAL_CROSS = "INTERNAL_CROSS", "Internal cross"
    INTERNAL_SELECTION = "INTERNAL_SELECTION", "Internal selection"
    EXTERNAL_ACCESSION = "EXTERNAL_ACCESSION", "External accession"
    WILD_COLLECTION = "WILD_COLLECTION", "Wild collection"
    DONATION = "DONATION", "Donation"
    PURCHASE = "PURCHASE", "Purchase"
    UNKNOWN = "UNKNOWN", "Unknown"


class BiologicalStatus(models.TextChoices):
    """MCPD SAMPSTAT, collapsed to the levels that matter here."""

    WILD = "WILD", "Wild (100)"
    WEEDY = "WEEDY", "Weedy (200)"
    LANDRACE = "LANDRACE", "Landrace (300)"
    BREEDING_MATERIAL = "BREEDING_MATERIAL", "Breeding/research material (400)"
    ADVANCED_CULTIVAR = "ADVANCED_CULTIVAR", "Advanced / improved cultivar (500)"
    GENETIC_STOCK = "GENETIC_STOCK", "Genetic stock (600)"
    OTHER = "OTHER", "Other (999)"


class NameType(models.TextChoices):
    BREEDER_CODE = "BREEDER_CODE", "Breeder code"
    ACCESSION_NUMBER = "ACCESSION_NUMBER", "Accession number"
    PI_NUMBER = "PI_NUMBER", "USDA PI number"
    GRIN_ID = "GRIN_ID", "GRIN identifier"
    CULTIVAR_NAME = "CULTIVAR_NAME", "Cultivar name"
    NICKNAME = "NICKNAME", "Nickname / working name"
    DOI = "DOI", "DOI"
    OTHER = "OTHER", "Other"


class ParentageRole(models.TextChoices):
    FEMALE = "FEMALE", "Female / seed parent"
    MALE = "MALE", "Male / pollen parent"
    RECURRENT = "RECURRENT", "Recurrent parent"
    DONOR = "DONOR", "Donor parent"
    OPEN_POLLINATED = "OPEN_POLLINATED", "Open-pollinated (pollen cloud)"
    SELF = "SELF", "Self"
    UNKNOWN = "UNKNOWN", "Unknown"


class GenotypeOrigin(models.TextChoices):
    SEEDLING = "SEEDLING", "Seedling"
    CLONAL_SELECTION = "CLONAL_SELECTION", "Clonal selection"
    LANDRACE_SELECTION = "LANDRACE_SELECTION", "Landrace selection"
    MUTATION = "MUTATION", "Mutation / sport"
    DOUBLED_HAPLOID = "DOUBLED_HAPLOID", "Doubled haploid"
    INTROGRESSION = "INTROGRESSION", "Introgression line"
    UNKNOWN = "UNKNOWN", "Unknown"


class PlantStatus(models.TextChoices):
    ALIVE = "ALIVE", "Alive"
    DEAD = "DEAD", "Dead"
    REMOVED = "REMOVED", "Removed"
    MISSING = "MISSING", "Missing"
    UNKNOWN = "UNKNOWN", "Unknown"


class ComponentRole(models.TextChoices):
    ROOTSTOCK = "ROOTSTOCK", "Rootstock"
    INTERSTEM = "INTERSTEM", "Interstem"
    SCION = "SCION", "Scion"
    OWN_ROOT = "OWN_ROOT", "Own root"


class PropagationMethod(models.TextChoices):
    GRAFT = "GRAFT", "Graft"
    CHIP_BUD = "CHIP_BUD", "Chip budding"
    T_BUD = "T_BUD", "T-budding"
    CUTTING = "CUTTING", "Cutting"
    DIVISION = "DIVISION", "Division"
    SEEDLING = "SEEDLING", "Seedling"
    TISSUE_CULTURE = "TISSUE_CULTURE", "Tissue culture"
    LAYERING = "LAYERING", "Layering"
    UNKNOWN = "UNKNOWN", "Unknown"


class MatingDesign(models.TextChoices):
    POLYCROSS = "POLYCROSS", "Polycross"
    HALF_DIALLEL = "HALF_DIALLEL", "Half diallel"
    FULL_DIALLEL = "FULL_DIALLEL", "Full diallel"
    NC1 = "NC1", "North Carolina I"
    NC2 = "NC2", "North Carolina II"
    LINE_BY_TESTER = "LINE_BY_TESTER", "Line × tester"
    OPEN_POLLINATED = "OPEN_POLLINATED", "Open-pollinated"
    MASS_SELECTION = "MASS_SELECTION", "Mass selection"
    SINGLE_CROSS = "SINGLE_CROSS", "Single cross"
    THREE_WAY = "THREE_WAY", "Three-way cross"
    BACKCROSS = "BACKCROSS", "Backcross"
    OTHER = "OTHER", "Other"


class ListType(models.TextChoices):
    CROSSING_BLOCK = "CROSSING_BLOCK", "Crossing block"
    PANEL = "PANEL", "Panel"
    TRAINING_SET = "TRAINING_SET", "Training set"
    NURSERY = "NURSERY", "Nursery"
    TRIAL_ENTRIES = "TRIAL_ENTRIES", "Trial entries"
    WORKING_SET = "WORKING_SET", "Working set"
    CUSTOM = "CUSTOM", "Custom"
