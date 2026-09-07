"""Germplasm domain model.

Tiers: Crop -> Taxon -> Germplasm (named material) -> Genotype (genetic
individual) -> Plant (physical) -> PlantComponent (graft slots).

Cross-app foreign keys to apps that are not designed yet are deferred and
marked ``TODO``: ``Parentage.source_cross`` (breeding.Cross),
``Plant.source_batch`` and ``PlantComponent.seed_lot`` (inventory).
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from prefix_id import PrefixIDField

from apps.core.models import BaseModel

from . import enums


class Crop(BaseModel):
    """A breeding target, grouping one or more taxa (crop + wild relatives)."""

    id = PrefixIDField(prefix="crop", primary_key=True)
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Taxon(BaseModel):
    id = PrefixIDField(prefix="txn", primary_key=True)
    crop = models.ForeignKey(
        Crop,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="taxa",
    )
    genus = models.CharField(max_length=120)
    species = models.CharField(max_length=120, blank=True)
    subtaxon_rank = models.CharField(
        max_length=20, blank=True, help_text="subsp., var., f., ..."
    )
    subtaxon_name = models.CharField(max_length=120, blank=True)
    authority = models.CharField(max_length=200, blank=True)
    common_name = models.CharField(max_length=120, blank=True)
    ploidy = models.CharField(max_length=30, blank=True, help_text='e.g. "2n=6x=42"')
    mating_system = models.CharField(
        max_length=10,
        choices=enums.MatingSystem.choices,
        default=enums.MatingSystem.UNKNOWN,
    )
    growth_habit = models.CharField(
        max_length=10, choices=enums.GrowthHabit.choices, blank=True
    )
    is_perennial = models.BooleanField(default=True)

    class Meta:
        ordering = ["genus", "species", "subtaxon_name"]
        verbose_name_plural = "taxa"
        constraints = [
            models.UniqueConstraint(
                fields=["genus", "species", "subtaxon_rank", "subtaxon_name"],
                name="unique_taxon_name",
            )
        ]

    def __str__(self):
        parts = [self.genus, self.species, self.subtaxon_rank, self.subtaxon_name]
        return " ".join(p for p in parts if p)


class Germplasm(BaseModel):
    """Umbrella record for named genetic material at any level."""

    id = PrefixIDField(prefix="gp", primary_key=True)
    name = models.CharField(max_length=255, db_index=True)
    germplasm_type = models.CharField(
        max_length=30,
        choices=enums.GermplasmType.choices,
        default=enums.GermplasmType.UNKNOWN,
    )
    material_use = models.CharField(
        max_length=10,
        choices=enums.MaterialUse.choices,
        default=enums.MaterialUse.NA,
        help_text="Orthogonal to germplasm_type; flags rootstock vs scion material.",
    )
    taxon = models.ForeignKey(
        Taxon,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="germplasm",
    )
    program = models.ForeignKey(
        "core.Program",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="germplasm",
    )

    status = models.CharField(
        max_length=15,
        choices=enums.GermplasmStatus.choices,
        default=enums.GermplasmStatus.ACTIVE,
    )
    merged_into = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="merged_from",
        help_text="Set when this record is a duplicate folded into another.",
    )

    # --- Provenance ---
    source_type = models.CharField(
        max_length=25,
        choices=enums.SourceType.choices,
        default=enums.SourceType.UNKNOWN,
    )
    source_institute = models.CharField(max_length=200, blank=True)
    acquisition_date = models.DateField(null=True, blank=True)
    collecting_site = models.ForeignKey(
        "locations.Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collected_germplasm",
    )
    donor = models.CharField(max_length=200, blank=True)

    # --- Passport (hot MCPD fields + full dump) ---
    biological_status = models.CharField(
        max_length=25, choices=enums.BiologicalStatus.choices, blank=True
    )
    origin_country = models.CharField(
        max_length=3, blank=True, help_text="ISO 3166-1 alpha-3"
    )
    collection_date = models.DateField(null=True, blank=True)
    collector = models.CharField(max_length=200, blank=True)
    passport = models.JSONField(
        default=dict, blank=True, help_text="Full MCPD record as imported."
    )

    pedigree_string = models.TextField(
        blank=True, help_text="Free-text (Purdy) pedigree; import artifact."
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["germplasm_type"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name


class PopulationDetail(BaseModel):
    """1:1 extension of Germplasm for population-genetics attributes."""

    id = PrefixIDField(prefix="popd", primary_key=True)
    germplasm = models.OneToOneField(
        Germplasm, on_delete=models.CASCADE, related_name="population_detail"
    )
    base_population = models.ForeignKey(
        Germplasm,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="derived_populations",
    )
    cycle_number = models.PositiveSmallIntegerField(null=True, blank=True)
    cycle_label = models.CharField(max_length=20, blank=True, help_text='e.g. "C3"')
    mating_design = models.CharField(
        max_length=20, choices=enums.MatingDesign.choices, blank=True
    )
    effective_size = models.PositiveIntegerField(null=True, blank=True, help_text="Ne")
    num_parents = models.PositiveIntegerField(null=True, blank=True)
    selection_method = models.CharField(max_length=120, blank=True)
    selection_intensity = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, help_text="percent"
    )

    def __str__(self):
        return f"{self.germplasm.name} · population detail"


class GermplasmName(BaseModel):
    """Alternative names / external identifiers for a Germplasm record."""

    id = PrefixIDField(prefix="gpn", primary_key=True)
    germplasm = models.ForeignKey(
        Germplasm, on_delete=models.CASCADE, related_name="names"
    )
    name_type = models.CharField(max_length=20, choices=enums.NameType.choices)
    value = models.CharField(max_length=255, db_index=True)
    namespace = models.CharField(
        max_length=100, blank=True, help_text="Owning institution / registry."
    )
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["germplasm", "name_type"]
        constraints = [
            models.UniqueConstraint(
                fields=["name_type", "value", "namespace"],
                name="uniq_germplasm_name",
            ),
            models.UniqueConstraint(
                fields=["germplasm"],
                condition=models.Q(is_primary=True),
                name="uniq_primary_name_per_germplasm",
            ),
        ]

    def __str__(self):
        return f"{self.value} ({self.get_name_type_display()})"


class Genotype(BaseModel):
    """A distinct genetic identity within a Germplasm — the genome shared by
    one seedling and everything vegetatively propagated from it.

    Not a physical plant: every clonal ramet (graft, cutting, division) of the
    same individual points at one Genotype; see ``Plant`` for the physical
    unit. ``clonal_parent`` is only used when a sport / somatic mutation earns
    its own identity.
    """

    id = PrefixIDField(prefix="gt", primary_key=True)
    code = models.CharField(max_length=100, db_index=True)
    germplasm = models.ForeignKey(
        Germplasm, on_delete=models.PROTECT, related_name="genotypes"
    )
    origin = models.CharField(
        max_length=20,
        choices=enums.GenotypeOrigin.choices,
        default=enums.GenotypeOrigin.UNKNOWN,
    )
    clonal_parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="clonal_descendants",
    )
    selection_date = models.DateField(null=True, blank=True)
    selected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="selected_genotypes",
    )
    status = models.CharField(
        max_length=15,
        choices=enums.GermplasmStatus.choices,
        default=enums.GermplasmStatus.ACTIVE,
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(fields=["code"], name="uniq_genotype_code"),
        ]

    def __str__(self):
        return self.code


class Parentage(BaseModel):
    """One edge of the sexual pedigree DAG (parent -> child)."""

    id = PrefixIDField(prefix="par", primary_key=True)
    child = models.ForeignKey(
        Germplasm, on_delete=models.CASCADE, related_name="parent_edges"
    )
    parent = models.ForeignKey(
        Germplasm,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="child_edges",
        help_text="Null only when role=OPEN_POLLINATED (no single identifiable parent).",
    )
    role = models.CharField(
        max_length=20,
        choices=enums.ParentageRole.choices,
        default=enums.ParentageRole.UNKNOWN,
    )
    parent_genotype = models.ForeignKey(
        Genotype,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="parentage_edges",
        help_text="The specific parent genotype, when known (crossing-block clone).",
    )
    # TODO(breeding): source_cross = FK("breeding.Cross", null=True) for provenance
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["child", "role"]
        constraints = [
            models.UniqueConstraint(
                fields=["child", "parent", "role"], name="uniq_parentage_edge"
            ),
            models.UniqueConstraint(
                fields=["child"],
                condition=models.Q(role=enums.ParentageRole.FEMALE),
                name="uniq_female_parent_per_child",
            ),
            models.UniqueConstraint(
                fields=["child"],
                condition=models.Q(role=enums.ParentageRole.OPEN_POLLINATED),
                name="uniq_open_pollinated_per_child",
            ),
            models.CheckConstraint(
                condition=~models.Q(child=models.F("parent")),
                name="parentage_no_self_loop",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(role=enums.ParentageRole.OPEN_POLLINATED)
                    | models.Q(parent__isnull=False)
                ),
                name="parentage_parent_required_unless_open_pollinated",
            ),
        ]
        indexes = [
            models.Index(fields=["parent"]),
            models.Index(fields=["child"]),
        ]

    def __str__(self):
        parent = self.parent or "pollen cloud"
        return f"{parent} --{self.role}--> {self.child}"


class Plant(BaseModel):
    """A physical, individually tracked plant (tree, crown, ...).

    Every Plant has at least one PlantComponent (enforced at the form /
    serializer layer). ``primary_genotype`` is a denormalised convenience for
    the own-root or scion genotype; the components are the source of truth.
    """

    id = PrefixIDField(prefix="plt", primary_key=True)
    label = models.CharField(max_length=100, db_index=True)
    primary_genotype = models.ForeignKey(
        Genotype,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="plants",
    )
    location = models.ForeignKey(
        "locations.Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="plants",
    )
    established_date = models.DateField(null=True, blank=True)
    propagation_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=enums.PlantStatus.choices,
        default=enums.PlantStatus.ALIVE,
    )
    removal_date = models.DateField(null=True, blank=True)
    removal_reason = models.CharField(max_length=255, blank=True)
    parent_plant = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="propagules",
        help_text="Plant this one was divided / propagated from.",
    )
    # TODO(inventory): source_batch = FK("inventory.PropagationBatch", null=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["label"]

    def __str__(self):
        return self.label

    @property
    def is_grafted(self):
        roles = {c.role for c in self.components.all()}
        return bool(roles & {enums.ComponentRole.ROOTSTOCK, enums.ComponentRole.SCION})


class PlantComponent(BaseModel):
    """One genetic component in a plant's graft stack (or its own root)."""

    id = PrefixIDField(prefix="pcmp", primary_key=True)
    plant = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name="components"
    )
    role = models.CharField(max_length=12, choices=enums.ComponentRole.choices)
    position = models.PositiveSmallIntegerField(
        default=0, help_text="0 = rootstock, ascending; multiple scions allowed."
    )
    source_germplasm = models.ForeignKey(
        Germplasm, on_delete=models.PROTECT, related_name="plant_components"
    )
    source_genotype = models.ForeignKey(
        Genotype,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="plant_components",
        help_text="Null = a seedling of source_germplasm, genotype not yet minted.",
    )
    # TODO(inventory): seed_lot = FK("inventory.SeedLot", null=True)
    propagation_method = models.CharField(
        max_length=15,
        choices=enums.PropagationMethod.choices,
        default=enums.PropagationMethod.UNKNOWN,
    )
    propagated_from = models.ForeignKey(
        Plant,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="propagated_components",
        help_text="Source plant of the scion wood / cutting / division.",
    )
    grafted_on = models.DateField(null=True, blank=True)
    removed_on = models.DateField(
        null=True, blank=True, help_text="Set when top-worked over / removed."
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["plant", "position"]
        constraints = [
            models.UniqueConstraint(
                fields=["plant", "role", "position"], name="uniq_component_slot"
            ),
        ]

    def __str__(self):
        return f"{self.plant.label} · {self.get_role_display()}"

    @property
    def is_active(self):
        return self.removed_on is None

    def clean(self):
        # OWN_ROOT and ROOTSTOCK are mutually exclusive on one plant.
        if self.role in (
            enums.ComponentRole.OWN_ROOT,
            enums.ComponentRole.ROOTSTOCK,
        ):
            conflict = (
                enums.ComponentRole.ROOTSTOCK
                if (self.role == enums.ComponentRole.OWN_ROOT)
                else enums.ComponentRole.OWN_ROOT
            )
            clash = PlantComponent.objects.filter(
                plant=self.plant, role=conflict
            ).exclude(pk=self.pk)
            if clash.exists():
                raise ValidationError(
                    f"A plant cannot have both {enums.ComponentRole.OWN_ROOT} "
                    f"and {enums.ComponentRole.ROOTSTOCK} components."
                )


class GermplasmList(BaseModel):
    """A named, ordered working set of germplasm."""

    id = PrefixIDField(prefix="gpl", primary_key=True)
    name = models.CharField(max_length=200)
    list_type = models.CharField(
        max_length=20,
        choices=enums.ListType.choices,
        default=enums.ListType.CUSTOM,
    )
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="germplasm_lists",
    )
    program = models.ForeignKey(
        "core.Program",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="germplasm_lists",
    )
    is_locked = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GermplasmListItem(BaseModel):
    id = PrefixIDField(prefix="gpli", primary_key=True)
    germplasm_list = models.ForeignKey(
        GermplasmList, on_delete=models.CASCADE, related_name="items"
    )
    germplasm = models.ForeignKey(
        Germplasm, on_delete=models.CASCADE, related_name="list_memberships"
    )
    position = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["germplasm_list", "position"]
        constraints = [
            models.UniqueConstraint(
                fields=["germplasm_list", "germplasm"],
                name="uniq_list_membership",
            ),
        ]

    def __str__(self):
        return f"{self.germplasm_list.name}: {self.germplasm.name}"
