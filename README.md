# Persist

Django implementation of the Persist plant breeding data management
application, focused on perennial crops.

## Stack

- Django 6 + Django REST Framework (admin-first UI for now)
- PostgreSQL 17 / PostGIS 3.5
- `uv` for dependency management, `ruff` for lint/format, `pytest-django` for tests

## Layout

```
persist/            project package: settings/, urls.py, wsgi/asgi, api router
apps/
  core/             abstract base models (UUID pk + timestamps), shared mixins
  accounts/         custom User model (AUTH_USER_MODEL = "accounts.User")
  germplasm/        accessions / genets, clonal identity
  breeding/         crosses, populations, selections, pedigree graph
  traits/           trait / observation-variable ontology
  trials/           studies, plots, entries, field layout
  phenotyping/      longitudinal observation measurements
  genomics/         markers, marker sets, genotype calls
  inventory/        seed lots, stocks, storage transactions
  locations/        sites, fields, plot geometry (PostGIS), weather
```

Implemented so far: `core` (Program, Organization, Address), `accounts`,
`germplasm`, a stub `locations.Location`, and `inventory` storage/stock
models. The other apps are still empty.

## Domain notes

- **Organization** is the top-level grouping: a university, company, agency,
  etc. It can have many people, storage sites, locations, programs,
  germplasm, trials, and phenotyping / genotyping events.
- **Storage sites** belong to an organization and hold a tree of **storage
  locations**: greenhouses, growth chambers, field sites, freezer rooms,
  fridges, etc. Locations nest (freezer room > freezer > shelf > box >
  sample), and a site can be tied to a geographic `Location` and/or an
  `Address`.

## Getting started

```bash
# 1. Tooling (uv via mise, or the standalone installer)
mise use -g uv            # or: curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Dependencies + env
uv sync
cp .env.example .env

# 3. Database
make db-up                # starts the PostGIS container

# 4. Migrate + run
make migrations
make migrate
make superuser
make run                  # http://127.0.0.1:8000/admin/
```

GeoDjango needs system GDAL/GEOS/PROJ libraries available to the Python
process (e.g. `gdal`, `geos`, `proj` packages). Set `GDAL_LIBRARY_PATH` /
`GEOS_LIBRARY_PATH` in `.env` if they aren't auto-detected.

## Settings

`DJANGO_SETTINGS_MODULE` selects the environment module:

- `persist.settings.dev` — default for `manage.py`, debug toolbar on
- `persist.settings.prod` — default for `wsgi`/`asgi`, security headers on
- `persist.settings.test` — used by `pytest`
