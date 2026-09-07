"""Root URL configuration.

App-specific routes live in ``apps/<app>/urls.py`` (added as each app grows a
UI/API surface). REST endpoints are mounted under ``/api/`` via the router in
``persist.api``.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from persist.api import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
