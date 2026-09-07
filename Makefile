.PHONY: help install db-up db-down migrate migrations run shell test lint fmt superuser

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install:  ## Sync the virtualenv from pyproject/uv.lock
	uv sync

db-up:  ## Start the PostGIS container
	docker compose up -d db

db-down:  ## Stop the PostGIS container
	docker compose down

migrations:  ## Create migrations from model changes
	uv run python manage.py makemigrations

migrate:  ## Apply migrations
	uv run python manage.py migrate

run:  ## Run the dev server
	uv run python manage.py runserver

shell:  ## Django shell_plus (django-extensions)
	uv run python manage.py shell_plus

superuser:  ## Create an admin user
	uv run python manage.py createsuperuser

test:  ## Run the test suite
	uv run pytest

lint:  ## Lint with ruff
	uv run ruff check .

fmt:  ## Format with ruff
	uv run ruff format .
