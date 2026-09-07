"""Base settings shared by every environment.

Environment-specific modules (``dev``, ``prod``, ``test``) import ``*`` from
here and override as needed. Configuration is read from the environment via
``django-environ``; see ``.env.example``.
"""

from pathlib import Path

import environ

# persist/settings/base.py -> repo root is three parents up.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_USE_GIS=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-only-insecure-key")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")

# GeoDjango needs system GDAL/GEOS/PROJ libraries on every machine that runs it.
# Keep it off until geometry fields land in the `locations` app; flip
# DJANGO_USE_GIS=True (after installing the libs) to switch on the PostGIS
# backend and django.contrib.gis.
USE_GIS = env("DJANGO_USE_GIS")


# --- Applications ---------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
if USE_GIS:
    DJANGO_APPS.append("django.contrib.gis")

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "django_extensions",
]

LOCAL_APPS = [
    "apps.core",
    "apps.accounts",
    "apps.germplasm",
    "apps.breeding",
    "apps.traits",
    "apps.trials",
    "apps.phenotyping",
    "apps.genomics",
    "apps.inventory",
    "apps.locations",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "persist.urls"
WSGI_APPLICATION = "persist.wsgi.application"
ASGI_APPLICATION = "persist.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# --- Database ----------------------------------------------------------------
# The server is PostgreSQL/PostGIS either way; the Django engine follows USE_GIS.

DATABASES = {
    "default": env.db_url(
        "DATABASE_URL",
        default="postgres://persist:persist@localhost:5432/persist",
    ),
}
DATABASES["default"]["ENGINE"] = (
    "django.contrib.gis.db.backends.postgis"
    if USE_GIS
    else "django.db.backends.postgresql"
)


# --- Auth ------------------------------------------------------------------

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Internationalization --------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# --- Static / media ------------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Django REST Framework -----------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
}
