from django.contrib import admin

from .models import (
    Crop,
    Genotype,
    Germplasm,
    GermplasmList,
    GermplasmListItem,
    GermplasmName,
    Parentage,
    Plant,
    PlantComponent,
    PopulationDetail,
    Taxon,
)


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Taxon)
class TaxonAdmin(admin.ModelAdmin):
    list_display = ("__str__", "common_name", "crop", "mating_system", "is_perennial")
    list_filter = ("crop", "mating_system", "growth_habit", "is_perennial")
    search_fields = ("genus", "species", "common_name")
    autocomplete_fields = ("crop",)


class PopulationDetailInline(admin.StackedInline):
    model = PopulationDetail
    fk_name = "germplasm"
    extra = 0
    autocomplete_fields = ("base_population",)


class GermplasmNameInline(admin.TabularInline):
    model = GermplasmName
    extra = 1


class ParentageChildInline(admin.TabularInline):
    """Edges where this germplasm is the child (i.e. its parents)."""

    model = Parentage
    fk_name = "child"
    extra = 0
    autocomplete_fields = ("parent", "parent_genotype")
    verbose_name = "parent edge"
    verbose_name_plural = "parents"


@admin.register(Germplasm)
class GermplasmAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "germplasm_type",
        "material_use",
        "taxon",
        "program",
        "status",
    )
    list_filter = ("germplasm_type", "material_use", "status", "source_type", "program")
    search_fields = ("name", "names__value", "pedigree_string")
    autocomplete_fields = ("taxon", "program", "merged_into", "collecting_site")
    inlines = (PopulationDetailInline, GermplasmNameInline, ParentageChildInline)


@admin.register(Genotype)
class GenotypeAdmin(admin.ModelAdmin):
    list_display = ("code", "germplasm", "origin", "status", "selection_date")
    list_filter = ("origin", "status")
    search_fields = ("code", "germplasm__name")
    autocomplete_fields = ("germplasm", "clonal_parent", "selected_by")


@admin.register(Parentage)
class ParentageAdmin(admin.ModelAdmin):
    list_display = ("child", "role", "parent", "parent_genotype")
    list_filter = ("role",)
    search_fields = ("child__name", "parent__name")
    autocomplete_fields = ("child", "parent", "parent_genotype")


class PlantComponentInline(admin.TabularInline):
    model = PlantComponent
    fk_name = "plant"
    extra = 1
    autocomplete_fields = ("source_germplasm", "source_genotype", "propagated_from")


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "primary_genotype",
        "location",
        "status",
        "established_date",
    )
    list_filter = ("status",)
    search_fields = ("label", "primary_genotype__code")
    autocomplete_fields = ("primary_genotype", "location", "parent_plant")
    inlines = (PlantComponentInline,)


class GermplasmListItemInline(admin.TabularInline):
    model = GermplasmListItem
    extra = 1
    autocomplete_fields = ("germplasm",)


@admin.register(GermplasmList)
class GermplasmListAdmin(admin.ModelAdmin):
    list_display = ("name", "list_type", "owner", "program", "is_locked")
    list_filter = ("list_type", "is_locked", "program")
    search_fields = ("name",)
    autocomplete_fields = ("owner", "program")
    inlines = (GermplasmListItemInline,)
