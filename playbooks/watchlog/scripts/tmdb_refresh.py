#!/usr/bin/env python3
"""
TMDB availability refresh for to-watch movies (nightly cron).

For each Movies/ note with status to-watch that is due, asks TMDB where the film can be
watched and writes three fields: `available` (true when any service in any country
streams, rents, sells or shows it free or with ads), `tmdb_id` (saves the IMDB lookup on
later runs) and `tmdb_checked` (the day). It also fills an empty `released` from TMDB's
release date. Nothing else in the note is touched.

A movie is due when it was never checked, when it is not available and was checked
UNAVAILABLE_TTL days ago or more (it may reach streaming any week), or when it is
available and was checked AVAILABLE_TTL days ago or more.

Needs TMDB_API_KEY in .env: either the v3 "API Key" or the "API Read Access Token".
Watch provider data is supplied to TMDB by JustWatch; the dashboard credits both.

Usage:
    python3 scripts/tmdb_refresh.py [--dry-run] [--limit N]
"""

import argparse
import importlib.util
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
API = 'https://api.themoviedb.org/3/'
UNAVAILABLE_TTL = 7
AVAILABLE_TTL = 30
RATE = 0.1          # seconds between requests, well under TMDB's limit
PROVIDER_KINDS = ('flatrate', 'rent', 'buy', 'free', 'ads')


def _load_vault_import():
    spec = importlib.util.spec_from_file_location('vault_import', Path(__file__).parent / 'import.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

vi = _load_vault_import()


class AuthError(Exception):
    pass


def available(providers: dict) -> bool:
    """True when any country lists any way to watch: subscription, rent, buy, free or ads."""
    return any(isinstance(v, dict) and any(v.get(k) for k in PROVIDER_KINDS) for v in providers.values())


def due(fm: dict, today: date) -> bool:
    last = fm.get('tmdb_checked', '')
    try:
        age = (today - date.fromisoformat(last)).days
    except ValueError:
        return True
    return age >= (AVAILABLE_TTL if fm.get('available') == 'true' else UNAVAILABLE_TTL)


def tmdb_get(path: str, key: str) -> dict:
    """GET an API path. A Read Access Token (a JWT, starting eyJ) goes in the header,
    a v3 API key in the query string."""
    url, headers = API + path, {'accept': 'application/json'}
    if key.startswith('eyJ'):
        headers['Authorization'] = f'Bearer {key}'
    else:
        url += ('&' if '?' in url else '?') + 'api_key=' + urllib.parse.quote(key)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise AuthError('TMDB refused the key (401); check TMDB_API_KEY in .env') from e
        raise


def lookup(imdb_id: str, tmdb_id: str, key: str) -> tuple[str, str, bool] | None:
    """(tmdb_id, release date, available) for a movie, or None when TMDB has no such movie."""
    release = ''
    if not tmdb_id:
        found = tmdb_get(f'find/{imdb_id}?external_source=imdb_id', key).get('movie_results') or []
        time.sleep(RATE)
        if not found:
            return None
        tmdb_id, release = str(found[0]['id']), found[0].get('release_date') or ''
    providers = tmdb_get(f'movie/{tmdb_id}/watch/providers', key).get('results') or {}
    time.sleep(RATE)
    return tmdb_id, release, available(providers)


def refresh(vault: Path, key: str, dry_run: bool, limit: int | None, today: date | None = None) -> dict:
    today = today or date.today()
    stats = {'checked': 0, 'available': 0, 'not_found': 0, 'errors': 0, 'skipped': 0}
    for md in sorted((vault / 'Movies').glob('*.md')):
        if limit is not None and stats['checked'] >= limit:
            break
        content = md.read_text(encoding='utf-8')
        fm, _ = vi.read_frontmatter(content)
        imdb_id = fm.get('imdb_id', '')
        if fm.get('status') != 'to-watch' or not imdb_id.startswith('tt') or not due(fm, today):
            stats['skipped'] += 1
            continue
        try:
            res = lookup(imdb_id, fm.get('tmdb_id', ''), key)
        except AuthError:
            raise
        except Exception as e:
            print(f'  Error {imdb_id}: {e}', file=sys.stderr)
            stats['errors'] += 1
            continue
        stats['checked'] += 1
        updates = {'tmdb_checked': str(today)}
        if res is None:
            stats['not_found'] += 1  # checked, so it waits UNAVAILABLE_TTL before the next try
        else:
            tmdb_id, release, avail = res
            updates.update({'tmdb_id': tmdb_id, 'available': 'true' if avail else 'false'})
            if release and not fm.get('released'):
                updates['released'] = release
            stats['available'] += avail
        if not dry_run:
            for k, v in updates.items():
                content = vi.update_field(content, k, v)
            md.write_text(content, encoding='utf-8')
    return stats


def main() -> None:
    p = argparse.ArgumentParser(description='Refresh TMDB availability on to-watch movies.')
    p.add_argument('--dry-run', action='store_true', help='Query TMDB but write no files')
    p.add_argument('--limit', type=int, default=None, help='Check at most N movies')
    args = p.parse_args()
    vi.load_env(VAULT_ROOT)
    key = os.environ.get('TMDB_API_KEY', '')
    if not key:
        sys.exit('Error: TMDB_API_KEY missing from .env')
    try:
        stats = refresh(VAULT_ROOT, key, args.dry_run, args.limit)
    except AuthError as e:
        sys.exit(f'Error: {e}')
    print(f"Done. Checked: {stats['checked']:,}, available: {stats['available']:,}, "
          f"not on TMDB: {stats['not_found']:,}, errors: {stats['errors']:,}, not due: {stats['skipped']:,}")


if __name__ == '__main__':
    main()
