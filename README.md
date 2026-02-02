# Fanfiction

[![Django CI](https://github.com/delitamakanda/fanfiction/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/delitamakanda/fanfiction/actions/workflows/django.yml)

> A fanfiction platform powered by a Django REST backend and a Vue.js/Ionic frontend.

## Table of contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Quick start](#quick-start)
  - [Backend (Django)](#backend-django)
  - [Frontend (Vue.js/Ionic)](#frontend-vuejsionic)
- [Background tasks](#background-tasks)
- [Translations](#translations)
- [Recommendation engine](#recommendation-engine)
- [Scraper](#scraper)
- [Testing](#testing)
- [Deployment](#deployment)
- [Additional resources](#additional-resources)

## Overview
This repository contains the source code for a bilingual fanfiction community. The Django
backend exposes a REST API, background workers and administrative interfaces, while the
Vue.js/Ionic application delivers the user-facing experience. Supporting utilities provide
recommendations, content import and automated notifications.

A live demo of the mobile web application is available at
[fanfiction-fr.netlify.app](https://fanfiction-fr.netlify.app/).

## Features
- Fanfiction catalogue with categories, tags, chapters, comments and user favourites.
- JWT/OAuth2-secured REST API built with Django REST Framework and Spectacular.
- Celery workers for scheduled notifications and account maintenance.
- Redis-backed recommendation engine based on user co-likes.
- Admin and moderation tooling for managing content and users.
- Internationalisation support and automated translation compilation.
- Modern stack targeting Django 5.1 and Python 3.12 deployments.

## Architecture
```
├── backend/        # Django project configuration and Celery entrypoint
├── api/            # REST API endpoints, serializers and services
├── fanfics/        # Core fanfiction models, scraping utilities, recommendation engine
├── chapters/, comments/, categories/, helpcenter/, posts/, forum/  # Domain apps
├── templates/, static/   # Django templates and static assets
├── docs/           # Additional documentation and guidelines
└── frontend (Vue.js/Ionic)  # Separate project served from the same repository
```

## Requirements
- Python 3.12+
- Node.js 16+ and npm
- Redis (for Celery/recommendations) – optional during development
- A PostgreSQL database in production (SQLite is used by default for local dev)

## Quick start
Clone the repository and create the environment files (`.env`, `.env.production`, etc.) as
needed. Example configuration for local development:

```dotenv
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
CELERY_BROKER_URL=redis://localhost:6379/0
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

### Frontend (Vue.js/Ionic)
```bash
cd frontend

# Install dependencies
npm install

# Serve with hot reload at http://localhost:8080
npm run dev

# Build for production
npm run build

# Build with bundle analysis report
npm run build --report
```

## Background tasks
Celery workers power scheduled emails and periodic clean-up jobs. Run them alongside the web
server after configuring the broker URL:

```bash
celery -A backend worker -l info
celery -A backend beat -l info
```

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
The recommendation engine leverages Redis to track user likes and compute co-occurrence scores.
You can experiment with it from the Django shell:

```python
>>> from api.models import Fanfic
>>> from api.recommender import Recommender
>>> favourites = Fanfic.objects.filter(id__in=[1, 2])
>>> Recommender().suggest_fanfics_for(favourites)
[<Fanfic: Elementary>, <Fanfic: Nature>, ...]
```

## Scraper
Import fanfiction content from external sources using the scraper utilities:

```bash
python manage.py import_from_fanfiction_as_csv output_ccs.csv
python manage.py import_from_fanfiction_as_csv output_op.csv
python manage.py import_from_fanfiction_as_csv output_marvel.csv
```

See `fanfics/scraper.py` for commands that generate these CSV files.

## Testing
Run the test suite with coverage reporting:

```bash
coverage run --source=api --omit=*/migrations/* manage.py test
coverage report -m
```

For a quicker feedback loop you can also use Django's built-in test runner directly:

```bash
python manage.py test
```

## Deployment
For production deployment and running migrations on the Aliyun/Apsara database via SSH, see the [Deployment Guide](docs/deployment.md).

Key points:
- The `manage.py` script automatically detects production environment variables
- When Aliyun database variables are set, it uses production settings
- Simply run `python manage.py migrate` on the production server

## Additional resources
- [Django documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery task queue](https://docs.celeryq.dev/)
- [Vue.js guide](https://vuejs.org/v2/guide/)
- [Ionic documentation](https://ionicframework.com/docs)
