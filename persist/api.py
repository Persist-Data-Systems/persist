"""Project-wide DRF router.

Each app registers its viewsets here as it gains an API, e.g.::

    from apps.germplasm.api import AccessionViewSet
    router.register("accessions", AccessionViewSet)
"""

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
