<!-- Copilot instructions tailored for the PopEll Top100 Django project -->
# Copilot / AI agent quick guide

This repository is a Django (4.x) web app that collects and publishes a "Top 100" hitlist. The guidance below focuses on immediately actionable knowledge for code edits, tests, and feature work.

- Project entry points: `manage.py` (dev), `popell_top100/settings.py` (dev) and `popell_top100/prod_settings.py` (production).
- Main app: `core/` — models in `core/models/`, business logic in `core/services/`, Spotify integration in `core/spotify/`, and views/templates under `core/views.py` and `templates/`.

Key architecture notes
- The app uses Django MVC: models under `core/models/`, views in `core/views.py` and REST endpoints under `core/rest_api`.
- Spotify is integrated via `core/spotify/spotify.py` which wraps spotipy. Domain adapters exist in `core/spotify/domain.py` and model conversion functions such as `Track.from_json` and `Track.from_model` are used.
- Services hold business rules: e.g. `core/services/tracks.py` (ArtistService, TrackService) and `core/services/voting.py` / `settings.py` for hitlist behaviour. Prefer adding logic into services rather than views.
- Hitlist lifecycle: `HitList` objects (models) + `HitListService` control opening/closing and exporting playlists (see `core/views.py` for usage examples).

Environment and dev workflows
- Development uses sqlite by default (see `popell_top100/settings.py`). Production uses Postgres configured in `prod_settings.py` via environment variables.
- Recommended dev setup (from repository README): use pipenv, then `pipenv shell` and `pipenv install --ignore-pipfile --dev`. Tests run with pytest (see `tests/`).
- Before running Spotify flows, set these environment variables in dev: `DJANGO_SECRET`, `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIPY_REDIRECT_URI`.
- Run the dev server with `python manage.py runserver` after activating the virtualenv.

Testing and quality
- Tests live under `tests/` and exercise forms, views and the Spotify domain adapters. Use the existing test structure when adding tests: small, focused unit tests that import models/services directly.
- Pre-commit hooks are recommended (black, flake8). The README documents installing `pre-commit install`.

Patterns & conventions (project-specific)
- Business logic belongs in `core/services/*`. Views should orchestrate forms/services and return templates/JSON.
- Spotify external calls are wrapped in `core/spotify/spotify.py`. Use `core/spotify/domain.py` for serializing/deserializing Spotify payloads into lightweight dataclasses.
- Non-Spotify (custom) tracks are represented by model flags `is_non_spotify`. Services must preserve this flag (see `TrackService.create_custom_track`).
- Database access in services uses Django ORM patterns (`get_or_create`, `transaction.atomic` for multi-step ops such as `merge_tracks`). Follow the same style and minimal raw SQL.

Important files to reference when making changes
- `core/views.py` — examples of view patterns, spotify oauth flow and hitlist endpoints.
- `core/services/tracks.py` — artist/track creation, merging votes, and when to call Spotify domain adapters.
- `core/spotify/spotify.py` and `core/spotify/domain.py` — where external API is wrapped and converted.
- `core/models/` — track, artist and voting model details and flags like `is_non_spotify`.
- `tests/` — examples of how to test domain and Spotify wrappers.

Quick examples
- To add a new API endpoint that returns track metadata, follow `SpotipyGetView` in `core/views.py` and call `core.spotify.spotify.get_track_by_uri` which returns a domain `Track` dataclass.
- To modify merge behavior, edit `TrackService.merge_tracks` in `core/services/tracks.py`. It uses `transaction.atomic` and moves votes before deleting the source track.

Do NOTs for the agent
- Do not change production settings directly — prefer editing behavior in services or views and keep configuration via env vars and `prod_settings.py`.
- Avoid introducing global mutable state; session and request-scoped data (like Spotify tokens) are stored in Django sessions: `request.session["spotify_token"]`.

If you need more context
- Read `README.md` for developer setup notes. Inspect `tests/` and `core/views.py` to see how behaviour is exercised.

If anything in this file is unclear or you need more examples, ask for specific areas to expand (tests, common refactors, or deployment steps).
