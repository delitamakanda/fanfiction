# Fanfiction

[![Django CI](https://github.com/delitamakanda/fanfiction/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/delitamakanda/fanfiction/actions/workflows/django.yml)

> A fanfiction platform powered by a Django REST backend and a separate Vue 3 frontend ([`fanfiction-front-vue`](https://github.com/delitamakanda/fanfiction-front-vue)).

## Table of contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Quick start](#quick-start)
  - [Backend (Django)](#backend-django)
- [Background tasks](#background-tasks)
- [Translations](#translations)
- [Recommendation engine](#recommendation-engine)
- [CSV import](#csv-import)
- [Testing](#testing)
- [Additional resources](#additional-resources)

## Overview
This repository contains the source code for a bilingual fanfiction community. The Django
backend exposes a REST API, background workers and administrative interfaces, while the
Vue.js application delivers the user-facing experience. Supporting utilities provide
recommendations, content import and automated notifications.

A live demo of the mobile web application is available at
[fanfics-fr.netlify.app](https://fanfics-fr.netlify.app/).

## Features
- Fanfiction catalogue with categories, tags, chapters, comments and user favourites.
- JWT-secured REST API built with Django REST Framework, documented with drf-spectacular.
- Celery workers for scheduled notifications and account maintenance.
- Recommendation engine based on user co-favourites ("readers who liked X also liked Y").
- Admin and moderation tooling for managing content and users.
- Internationalisation support and automated translation compilation.
- Modern stack targeting Django 6.* and Python 3.13 deployments.

## Architecture
```
├── backend/                 # Django project: settings, root URLs, Celery app, WSGI/ASGI
│   ├── settings/            # base.py + development.py / test.py / production.py
│   ├── api_urls.py          # /api/ hub (monitoring, JWT, /api/v1/<app>/, /api/forum/)
│   └── celery.py
├── apps/                    # Django applications (app labels unchanged: fanfics, chapters…)
│   ├── core/                # shared: permissions, pagination, OrderField, choices,
│   │                        # Markdown, template tags, health / system endpoints
│   ├── accounts/            # profiles, JWT login/signup, follows, notifications, contact
│   ├── fanfics/             # fanfics, likes, recommendations, PDF export, CSV import
│   ├── chapters/            # chapters, autosave, AI summary (OpenAI)
│   ├── comments/ categories/ posts/ helpcenter/ forum/
│   └── <app>/
│       ├── models.py        # models + QuerySets (`visible_to(user)`, `published()`…)
│       ├── services.py      # business logic, reused by views, tasks and commands
│       ├── api/             # serializers.py, views.py (thin), filters.py
│       ├── urls.py
│       ├── tasks.py         # Celery tasks (explicit names)
│       ├── management/commands/
│       └── tests/
├── templates/, static/, locale/
└── docs/
(the Vue 3 frontend lives in a separate project: fanfiction-front-vue)
```

Settings are picked with `DJANGO_SETTINGS_MODULE`: `manage.py` defaults to
`backend.settings.development` (`backend.settings.test` for `manage.py test`),
WSGI/ASGI default to `backend.settings.production`. `backend.settings_production` is kept
as a deprecated alias.

## Requirements
- Python 3.12+ (CI runs 3.12 and 3.13)
- Redis for Celery (optional during development)
- A PostgreSQL database in production (SQLite is used by default for local dev)

## Environment Variables
Settings read the environment (or a `.env` file) with `python-decouple`. See `.env.example`
(local), `.env.docker` (docker compose) and `.env.production.example`. In Docker, `entrypoint.sh`
also sources `/env/envs_export.sh` when it exists.

## Quick start
Clone the repository and create the environment files (`.env`, `.env.production`, etc.) as
needed. Example configuration for local development:

```bash
cp .env.example .env
```

### Backend (Django)
```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Apply migrations and create a superuser
python manage.py migrate
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

## Background tasks
Celery workers power scheduled emails and periodic clean-up jobs. Run them alongside the web
server after configuring the broker URL:

```bash
celery -A backend worker -l info
celery -A backend beat -l info
```

The schedule lives in `CELERY_BEAT_SCHEDULE` (`backend/settings/base.py`): login reminders,
deactivation of inactive accounts, daily refresh and purge of recommendations.

You can also combine worker and scheduler in a single process if required:

```bash
celery -A backend worker -l info -B
```

## Translations
The project ships with localisation resources. To update message files and compile them:

```bash
# Extract new strings (ignoring the virtual environment directory)
django-admin makemessages --ignore=.venv/*

# Compile the message catalogues
django-admin compilemessages
```

## Recommendation engine
Recommendations are computed from `UserFavorite` co-occurrences for users who gave their
consent (`AccountProfile.reco_consent_given`), stored in `Recommendation` and cached. A daily
Celery task refreshes them; the API serves them on `/api/v1/fanfics/recommendations/`.

```python
>>> from apps.fanfics import services
>>> services.compute_recommendations(user_id=1)
[{'id': 12, 'title': '...', 'synopsis': '...'}, ...]
```

## CSV import
Fanfictions previously scraped from fanfiction.net are stored as CSV files in
`apps/fanfics/management/commands/data/`. Import them (idempotent) with:

```bash
python manage.py populate_categories
python manage.py import_from_fanfiction_as_csv output_ccs.csv output_op.csv output_marvel.csv --author <username>
```

Other seed commands: `populate_subcategories`, `populate_faq`, `populate_lexique`, `board`
(forum boards), `seed_demo` (DEBUG only).

## Testing
Run the test suite with coverage reporting:

```bash
coverage run manage.py test
coverage report -m
```

For a quicker feedback loop you can also use Django's built-in test runner directly:

```bash
python manage.py test
python manage.py test apps.fanfics    # one app
```

Lint and format with Ruff (configuration in `pyproject.toml`):

```bash
ruff check . && ruff format --check .
```

## Demo data
```bash
python manage.py seed_demo   # DEBUG only — demo-admin / demo-author / demo-reader, password demo-password-123
```

## Agentic workflow
Issues are specs: a Claude agent refines them, implements one ticket at a time and opens a PR for human review. See [docs/agentic-workflow.md](docs/agentic-workflow.md).

## Additional resources
- [Django documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery task queue](https://docs.celeryq.dev/)
- [Vue 3 guide](https://vuejs.org/guide/)
