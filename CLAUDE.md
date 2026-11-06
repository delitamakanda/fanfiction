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
python manage.py test fanfics.test_seed_demo   # a single module
celery -A backend worker -l info -B # background tasks
docker compose up                   # full stack (.env.docker)
```

Settings read `.env` through `python-decouple`; without it `DEBUG` defaults to `True` and the database to SQLite (`db.sqlite3`). The cache is local memory, e-mails go to the console. OpenAI (chapter summaries) and reCAPTCHA (contact form) are external calls — always mock them in tests.

Lint/format: Ruff (config in `pyproject.toml`). The codebase is **not** clean yet (~250 Ruff errors, ~170 unformatted files), so only lint what you touch: `bash scripts/agent/lint-changed.sh --fix` then `--check` (compares to `origin/main`). Do not reformat untouched files.

**Indentation is mixed**: `.editorconfig` asks for tabs and about 35 Python files use them, the rest use 4 spaces. Keep the style of the file you edit; new files use spaces (Ruff format). `lint-changed.sh` lints tab-indented files but does not reformat them.

## Architecture

Django 6, Python 3.12/3.13 (CI matrix; `runtime.txt` is 3.12). Bilingual fanfiction platform: a DRF API consumed by a separate Vue.js/Ionic front (`http://localhost:5173`, fanfics-fr.netlify.app). Project package `backend/` (settings, URLs, Celery app with the beat schedule, sitemaps, S3 storage for production via `settings_production.py`).

- `api/` — URL hub (`/api/` root and health checks, `/api/auth/token/` JWT, `/api/v1/<app>/` resources, `/api/forum/`), shared permissions (`custompermission.py`), pagination, auth backends (`EmailAuthBackend`: login with the e-mail address), recommendation engine (`recommender.py`), Celery tasks.
- `fanfics/` — `Fanfic` (`status` `brouillon` / `publié`, `Fanfic.published` manager, `MultiSelectField` genres, `classement`, likes, `total_likes`, `views`), `Recommendation`, `UserFavorite`, scraper and CSV import, PDF export.
- `chapters/` — `Chapter` (ordered per fanfic with `api.fields.OrderField`, OpenAI summary endpoint). `comments/` — threaded `Comment`. `categories/` — `Category` / `SubCategory` / `EntityCategory` (slugged). `accounts/` — `AccountProfile` (created by a `post_save` signal), `Social`, `Notification`, `FollowUser`, `FollowStories`. `posts/`, `helpcenter/` (FAQ, lexicon), `forum/` (DRF + Django template views in `forum/templates/`).
- Auth: `django.contrib.auth` `User`; DRF authenticates with simplejwt (`Authorization: Bearer`). Default permission is **`AllowAny`**: each view must declare its own.
- i18n: `locale/` (`fr-fr`, `en-us`), `django.middleware.locale.LocaleMiddleware`.

### Known issues

- `Chapter.clean()` rejects every `brouillon` chapter (`save()` clears `published` for drafts, then `full_clean()` requires it), so draft chapters cannot be saved. `seed_demo` only creates published chapters.
- The fanfic list (`/api/v1/fanfics/`) returns drafts to anonymous users unless filtered on `status`.

## Conventions

- Business logic in models, managers or `services.py`; keep views and serializers thin.
- Every view that reads private data or writes declares `permission_classes` and checks ownership (`request.user`); drafts are never exposed to readers.
- Serializers: explicit `fields`, read-only owners / counters, strict validation.
- Critical multi-step writes in `transaction.atomic()`; counters with `F()`; watch for N+1 queries (`select_related` / `prefetch_related`).
- New models or fields come with a migration (`python manage.py makemigrations <app> --name <explicit_name>`); never edit existing migrations. `makemigrations --check` must stay clean.
- Tests live in the app (`tests.py`, `test_*.py` or an `api/tests/` package), using `TestCase` and `APIClient` (`force_authenticate`); cover the nominal case, a permission refusal and a validation error. Commands guarded by `DEBUG` need `@override_settings(DEBUG=True)` (the test runner forces `DEBUG=False`).
- User-facing API messages are mostly in French; templates use `{% translate %}`. Pages must stay usable on mobile and meet WCAG AA.
- `.claude/agents/` has project subagents: `test-writer`, `security-orm-reviewer`, `dependency-keeper`.

## Agentic workflow

Issues are specs: a Claude agent (GitHub Actions) refines them, implements one ticket at a time and opens a PR for human review. See `docs/agentic-workflow.md`. Agents must never modify `.github/`.
