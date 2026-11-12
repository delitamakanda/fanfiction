# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py seed_demo          # demo data (DEBUG only): demo-admin (staff) / demo-author / demo-reader, password demo-password-123
python manage.py runserver          # API http://localhost:8000/api/v1/ — Swagger /docs/swagger/, admin /admin/
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test               # Django test runner (TestCase / APIClient)
python manage.py test apps.fanfics.tests.test_seed_demo   # a single module
celery -A backend worker -l info -B # background tasks
docker compose up                   # full stack (.env.docker)
```

Settings are a package: `backend/settings/base.py` plus `development.py` (default of `manage.py`), `test.py` (default of `manage.py test`: in-memory SQLite, MD5 hasher, locmem e-mails, eager Celery) and `production.py` (default of WSGI/ASGI). `backend.settings_production` is a deprecated alias of `backend.settings.production`. Values come from the environment / `.env` (`python-decouple`); without `.env` the development settings use `DEBUG=True` and SQLite (`db.sqlite3`). OpenAI (chapter summaries) and reCAPTCHA (contact form) are external calls — always mock them in tests (`apps.chapters.services._openai_client`, `apps.accounts.services.verify_recaptcha`).

Lint/format: Ruff (config in `pyproject.toml`). The whole codebase is clean: keep `ruff check .` and `ruff format --check .` green (`bash scripts/agent/lint-changed.sh --fix` then `--check` only checks what changed against `origin/main`). Python files are indented with 4 spaces (`.editorconfig`).

## Architecture

Django 6, Python 3.12/3.13 (CI matrix; `runtime.txt` is 3.12). Bilingual fanfiction platform: a DRF API consumed by a separate Vue 3 front, `fanfiction-front-vue` (`http://localhost:5173`, fanfics-fr.netlify.app). Its URLs and response shapes are a contract: do not rename routes or fields it uses (`/api/auth/token/refresh/`, `/api/v1/accounts/{signup,login,logout,user,password-reset}/`, `/api/v1/categories/`, `/api/v1/categories/subcategory/`, `/api/v1/fanfics/`, `/api/v1/help/{faq,lexique}/`, `/api/v1/posts/`, `/api/health/`).

Project package `backend/`: settings package, root URLs, `api_urls.py` (the `/api/` hub, namespace `api`), `docs_urls.py` (Swagger), Celery app (`celery.py`, schedule in `CELERY_BEAT_SCHEDULE`), sitemaps, S3 storage. Apps live under `apps/` (`name = "apps.<app>"`, `label` unchanged so migrations and tables keep their names). URL names are namespaced: `api:<app>:<name>` (e.g. `api:fanfics:fanfic_pdf`, `api:forum:board_topics`).

- `apps/core/` — no models. `permissions.py` (`IsAdminOrReadOnly`, `IsOwnerOrReadOnly` / `IsOwner` reading `view.owner_field`), `pagination.py`, `fields.py` (`OrderField`), `choices.py` (`PublicationStatus`: `brouillon` / `publié`), `markdown.py` (`render_user_markdown`, raw HTML escaped), template tags (`filters`, `markdown`, `markdownify`, `gravatar`), monitoring views (`/api/`, `/api/health/`, `/api/health/detailed/`, `/api/system/`), `testing.py` (test factories).
- `apps/accounts/` — `AccountProfile` (created by a `post_save` signal), `Social`, `Notification`, `FollowUser`, `FollowStories`; `backends.EmailAuthBackend` (login with username or e-mail); `services.py` (follows, notifications, deactivation, password reset e-mail, contact form, reminders); Celery tasks.
- `apps/fanfics/` — `Fanfic` (`Fanfic.objects.visible_to(user)` / `.published()` / `.with_related()`, `Fanfic.published` manager, `MultiSelectField` genres, `classement`, likes with `total_likes`, `views`), `Recommendation`, `UserFavorite`; `services.py` (views counter, likes, share / report e-mails, recommendations); CSV import (`management/commands/data/`); PDF export; `seed_demo`.
- `apps/chapters/` — `Chapter` (ordered per fanfic with `OrderField`, `Chapter.objects.visible_to(user)`, `published` follows `status`); `services.py` (autosave, OpenAI summary). `apps/comments/` — threaded `Comment`. `apps/categories/` — `Category` / `SubCategory` / `EntityCategory` (slugged). `apps/posts/`, `apps/helpcenter/` (FAQ, lexicon, flat pages, embeddable HTML pages), `apps/forum/` (DRF + Django template views in `apps/forum/templates/`, `services.py`).
- Auth: `django.contrib.auth` `User` (always reference it through `settings.AUTH_USER_MODEL` / `get_user_model()`); DRF authenticates with simplejwt (`Authorization: Bearer`). Default permission is `IsAuthenticatedOrReadOnly`; each view still declares its own.
- Visibility: readers only see published fanfics and published chapters of published fanfics; authors also see their drafts (`visible_to`).
- i18n: `locale/` (`fr-fr`, `en-us`), `django.middleware.locale.LocaleMiddleware`.

## Conventions

- Business logic in models, QuerySets or `services.py`; keep views and serializers thin. Services raise `django.core.exceptions.ValidationError`; views turn it into a 400.
- Every view that reads private data or writes declares `permission_classes` and checks ownership (`request.user`); drafts are never exposed to readers.
- Serializers: explicit `fields`, read-only owners / counters, strict validation.
- Critical multi-step writes in `transaction.atomic()`; counters with `F()`; watch for N+1 queries (`select_related` / `prefetch_related`).
- New models or fields come with a migration (`python manage.py makemigrations <app> --name <explicit_name>`); never edit existing migrations. `makemigrations --check` must stay clean.
- Tests live in `apps/<app>/tests/` (`test_*.py`), using `TestCase` / `APITestCase` (`force_authenticate`) and the factories of `apps.core.testing` (`make_user`, `make_fanfic`, `make_chapter`…); cover the nominal case, a permission refusal and a validation error. Commands guarded by `DEBUG` need `@override_settings(DEBUG=True)` (test settings use `DEBUG=False`).
- Celery tasks use `@shared_task(name="<app>.tasks.<function>")`: the names are stored in the beat schedule, do not change them.
- User-facing API messages are mostly in French; templates use `{% translate %}`. Pages must stay usable on mobile and meet WCAG AA.
- `.claude/agents/` has project subagents: `test-writer`, `security-orm-reviewer`, `dependency-keeper`.

## Agentic workflow

Issues are specs: a Claude agent (GitHub Actions) refines them, implements one ticket at a time and opens a PR for human review. See `docs/agentic-workflow.md`. Agents must never modify `.github/`.
