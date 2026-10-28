#!/usr/bin/env python3
"""
Watchlog queue processor.

Reads _Queue.md, creates or updates notes via OMDB and TVmaze, then archives
processed entries above the --- divider.

Each line is either:
  https://www.imdb.com/title/ttXXXXXXX/           → add to watchlist
  https://www.imdb.com/title/ttXXXXXXX/ :: 8      → add/update with rating

Then applies the observation files the IMDB userscript writes to _data/imdb/
(see process_observations and userscript/imdb-sync.js).

Usage:
    python3 scripts/process_queues.py [--dry-run]
"""

import importlib.util
import json
import os
import re
import sys
import time
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Load shared helpers from import.py (can't use 'import' as module name)
# ---------------------------------------------------------------------------

def _load_vault_import():
    spec = importlib.util.spec_from_file_location(
        'vault_import', Path(__file__).parent / 'import.py'
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

vi = _load_vault_import()

QUEUE_NOTE = VAULT_ROOT / '_Queue.md'

IMDB_ID_RE  = re.compile(r'(tt\d+)')
DIVIDER_RE  = re.compile(r'^---\s*$', re.MULTILINE)
RATING_LINE = re.compile(r'(https?://[^\s]+)\s*::\s*(\d+(?:\.\d+)?)')


# ---------------------------------------------------------------------------
# Queue I/O
# ---------------------------------------------------------------------------

def read_queue(path: Path) -> tuple[list[str], str]:
    """Return (non-blank pending lines below ---, full raw content).

    Web Clipper appends to the end of the note, so pending entries land below
    the --- divider. The archive accumulates above it.
    """
    if not path.exists():
        return [], ''
    content = path.read_text(encoding='utf-8')
    parts = DIVIDER_RE.split(content, maxsplit=1)
    section = parts[1] if len(parts) > 1 else parts[0]
    lines = [l.strip() for l in section.splitlines()
             if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('<!--')]
    return lines, content


def archive_entries(path: Path, entries: list[str], content: str) -> None:
    """Remove processed entries from below --- and prepend them to the archive above."""
    if not entries:
        return
    today = str(date.today())
    m = DIVIDER_RE.search(content)
    if m:
        before = content[:m.start()]
        after  = content[m.end():]
    else:
        before = content
        after  = ''

    processed_set = set(entries)
    remaining = [l for l in after.splitlines() if l.strip() not in processed_set]

    new_content  = before.rstrip('\n') + '\n'
    new_content += f'<!-- {today} processed -->\n'
    new_content += '\n'.join(entries) + '\n'
    new_content += '---\n'
    remaining_text = '\n'.join(remaining).strip()
    if remaining_text:
        new_content += remaining_text + '\n'

    path.write_text(new_content, encoding='utf-8')


# ---------------------------------------------------------------------------
# TVmaze type detection (free, no rate limit)
# ---------------------------------------------------------------------------

def tvmaze_quick_lookup(imdb_id: str) -> dict | None:
    """Return raw TVmaze show object if found, None if not a known TV show.

    Uses the IMDB lookup endpoint — no quota, no key required.
    Result carries name, premiered, genres, averageRuntime for note building.
    """
    if not vi.HAS_REQUESTS:
        return None
    try:
        import requests
        r = requests.get(
            f'https://api.tvmaze.com/lookup/shows?imdb={imdb_id}',
            timeout=10,
        )
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"  TVmaze lookup error ({imdb_id}): {e}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# OMDB full fetch (richer than the enrichment-only fetch in import.py)
# ---------------------------------------------------------------------------

def omdb_full_fetch(imdb_id: str) -> dict:
    """Return all OMDB fields needed to create a note from scratch."""
    result = {'found': False}
    api_key = os.environ.get('OMDB_API_KEY', '')
    if not api_key or not vi.HAS_REQUESTS:
        return result
    try:
        import requests
        r = requests.get(
            'http://www.omdbapi.com/',
            params={'i': imdb_id, 'apikey': api_key},
            timeout=10,
        )
        if r.status_code != 200:
            return result
        data = r.json()
        if data.get('Response') != 'True':
            return result

        def clean(val):
            return '' if (val or '') == 'N/A' else (val or '')

        runtime_raw = clean(data.get('Runtime', ''))
        result = {
            'found':       True,
            'title':       clean(data.get('Title', '')),
            'year':        clean(data.get('Year', '')),
            'imdb_rating': clean(data.get('imdbRating', '')),
            'omdb_type':   clean(data.get('Type', '')),   # movie | series | episode
            'genres':      vi.parse_list(clean(data.get('Genre', ''))),
            'directors':   vi.parse_list(clean(data.get('Director', ''))),
            'runtime':     runtime_raw.replace(' min', '').strip(),
            'language':    clean(data.get('Language', '')),
            'country':     clean(data.get('Country', '')),
            'rated':       clean(data.get('Rated', '')),
            'metascore':   clean(data.get('Metascore', '')),
            'awards':      clean(data.get('Awards', '')),
            'writer':      clean(data.get('Writer', '')),
            'actors':      clean(data.get('Actors', '')),
            'poster':      clean(data.get('Poster', '')),
            'plot':        clean(data.get('Plot', '')),
        }
    except Exception as e:
        print(f"  OMDB error ({imdb_id}): {e}", file=sys.stderr)
    return result


# ---------------------------------------------------------------------------
# Note builders (queue version — no CSV row)
# ---------------------------------------------------------------------------

def _movie_fields(imdb_id: str, omdb: dict, my_rating: str, status: str, date_w: str) -> list:
    fields = [
        ('title',            omdb.get('title', '')),
        ('original_title',   omdb.get('title', '')),
        ('imdb_id',          imdb_id),
        ('imdb_url',         f'https://www.imdb.com/title/{imdb_id}/'),
        ('imdb_rating',      omdb.get('imdb_rating', '')),
        ('my_rating',        my_rating),
        ('year',             omdb.get('year', '')),
        ('type',             'movie'),
        ('genres',           omdb.get('genres', [])),
        ('directors',        omdb.get('directors', [])),
        ('runtime',          omdb.get('runtime', '')),
        ('status',           status),
        ('language',         omdb.get('language', '')),
        ('country',          omdb.get('country', '')),
        ('rated',            omdb.get('rated', '')),
        ('metascore',        omdb.get('metascore', '')),
        ('awards',           omdb.get('awards', '')),
        ('writer',           omdb.get('writer', '')),
        ('actors',           omdb.get('actors', '')),
        ('poster',           omdb.get('poster', '')),
        ('omdb_last_checked', str(date.today())),
    ]
    if date_w:
        fields.append(('date_watched', date_w))
    return fields


def _tv_fields(imdb_id: str, omdb: dict, tvmaze: dict, my_rating: str, status: str, date_w: str) -> list:
    fields = [
        ('title',               omdb.get('title', '')),
        ('original_title',      omdb.get('title', '')),
        ('imdb_id',             imdb_id),
        ('imdb_url',            f'https://www.imdb.com/title/{imdb_id}/'),
        ('imdb_rating',         omdb.get('imdb_rating', '')),
        ('my_rating',           my_rating),
        ('year',                omdb.get('year', '')),
        ('type',                'tv-series'),
        ('genres',              omdb.get('genres', [])),
        ('runtime',             omdb.get('runtime', '')),
        ('status',              status),
        ('tvmaze_id',           tvmaze.get('tvmaze_id', '')),
        ('total_seasons',       tvmaze.get('total_seasons', '')),
        ('series_status',       tvmaze.get('series_status', '')),
        ('following',           ''),
        ('current_season',      ''),
        ('last_season_watched', ''),
        ('next_season_start',   tvmaze.get('next_season_start', '')),
        ('next_season_date',    tvmaze.get('next_season_date', '')),
        ('tvmaze_last_checked', tvmaze.get('tvmaze_last_checked', '')),
        ('language',            tvmaze.get('language', '') or omdb.get('language', '')),
        ('network',             tvmaze.get('network', '')),
        ('country',             tvmaze.get('country', '')),
        ('show_type',           tvmaze.get('show_type', '')),
        ('premiered',           tvmaze.get('premiered', '')),
        ('ended',               tvmaze.get('ended', '')),
    ]
    if date_w:
        idx = next(i for i, (k, _) in enumerate(fields) if k == 'series_status')
        fields.insert(idx, ('date_watched', date_w))
    return fields


# ---------------------------------------------------------------------------
# Note creation
# ---------------------------------------------------------------------------

def create_note(imdb_id: str, my_rating: str, existing: dict, stats: dict, dry_run: bool,
                date_watched: str = '') -> bool | None:
    """Fetch metadata and write a new note. Returns True on success, False to retry later
    (OMDB unavailable), None for a title that never gets a note (an episode)."""
    print(f"  Creating: {imdb_id}")

    # Detect type via TVmaze (free, no quota). Movies return None.
    tv_show = tvmaze_quick_lookup(imdb_id)
    time.sleep(vi.TVMAZE_RATE)
    is_tv = tv_show is not None

    date_w = (date_watched or str(date.today())) if my_rating else ''

    if is_tv:
        title = tv_show.get('name') or imdb_id
        year  = (tv_show.get('premiered') or '')[:4] or 'unknown'

        # Build an omdb-shaped dict from TVmaze fields so _tv_fields() stays unchanged
        runtime_raw = tv_show.get('averageRuntime') or ''
        omdb_shaped = {
            'title':       title,
            'year':        year,
            'genres':      tv_show.get('genres') or [],
            'runtime':     str(runtime_raw) if runtime_raw else '',
            'imdb_rating': '',
        }

        tvmaze = vi.tvmaze_fetch(imdb_id, title, tvmaze_id=int(tv_show['id']))
        time.sleep(vi.TVMAZE_RATE)

        series_status = tvmaze.get('series_status', '')
        status = vi.resolve_tv_status('watched' if my_rating else 'to-watch', series_status, my_rating)
        fields = _tv_fields(imdb_id, omdb_shaped, tvmaze, my_rating, status, date_w)
        fields_dict = dict(fields)
        inferred = vi.infer_following(fields_dict.get('series_status', ''), my_rating)
        if inferred:
            fields = [(k, inferred if k == 'following' else v) for k, v in fields]
        summary = tvmaze.get('summary', '')
        body = '\n\n' + (summary + '\n\n' if summary else '') + vi.TV_SEASON_TABLE
        content = vi.format_frontmatter(fields) + body
        folder = 'TV Shows'
    else:
        # Movie: OMDB is required. If unavailable, leave entry in queue for retry.
        omdb = omdb_full_fetch(imdb_id)
        time.sleep(vi.OMDB_RATE)

        if not omdb['found']:
            print(f"  OMDB unavailable for {imdb_id} — leaving in queue to retry")
            stats['errors'] += 1
            return False

        if omdb.get('omdb_type') == 'episode':
            print(f"  Skipping episode: {imdb_id}")
            stats['skipped'] += 1
            return None

        title  = omdb.get('title') or imdb_id
        year   = omdb.get('year') or 'unknown'
        status = 'watched' if my_rating else 'to-watch'
        fields = _movie_fields(imdb_id, omdb, my_rating, status, date_w)
        content = vi.format_frontmatter(fields) + '\n'
        if omdb.get('plot'):
            content += '\n' + omdb['plot'] + '\n'
        folder = 'Movies'

    if not dry_run:
        dest_dir = VAULT_ROOT / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / vi.safe_filename(title, year)
        if dest.exists():
            dest = dest_dir / vi.safe_filename(f'{title} [{imdb_id}]', year)
        dest.write_text(content, encoding='utf-8')
        existing[imdb_id] = dest
        print(f"  → {dest.name}")

    stats['added'] += 1
    return True


def apply_rating(note_path: Path, imdb_id: str, my_rating: str, date_w: str, stats: dict, dry_run: bool) -> None:
    """Set my_rating on an existing note, with the status that follows from it.

    date_watched is only filled when empty, so a re-rating keeps the original date.
    Shared by the queue and the userscript observations, so both apply one rule."""
    note_content = note_path.read_text(encoding='utf-8')
    fm, _        = vi.read_frontmatter(note_content)
    existing_rating = fm.get('my_rating', '')

    if existing_rating == my_rating:
        print(f"  Rating unchanged ({my_rating}): {imdb_id}")
        stats['skipped'] += 1
        return

    print(f"  Updating rating {existing_rating or '—'} → {my_rating}: {imdb_id}")
    updates = {'my_rating': my_rating}

    if not fm.get('date_watched'):
        updates['date_watched'] = date_w

    if fm.get('series_status') is not None:
        series_status = fm.get('series_status', '')
        resolved = vi.resolve_tv_status(
            fm.get('status', ''), series_status, my_rating
        )
        if resolved != fm.get('status', ''):
            updates['status'] = resolved
    else:
        updates['status'] = 'watched'

    if not dry_run:
        for k, v in updates.items():
            note_content = vi.update_field(note_content, k, v)
        note_path.write_text(note_content, encoding='utf-8')

    stats['updated'] += 1


# ---------------------------------------------------------------------------
# Userscript observations (_data/imdb/*.json, written by userscript/imdb-sync.js)
# ---------------------------------------------------------------------------

OBS_SUBDIR      = Path('_data') / 'imdb'
OBS_KEEP_DAYS   = 30
DATE_RE         = re.compile(r'^\d{4}-\d{2}-\d{2}$')
IMDB_ONLY_RE    = re.compile(r'^tt\d+$')
ACTIONS_HEADER  = (
    '# Actions\n\n'
    'Things to do in or for this vault, not build (that goes in `_backlog/backlog.md`). '
    'Tick items off in Obsidian; Claude moves ticked items, with their indented lines, to '
    '`actions-done.md` in this folder the next time it edits this file.\n\n'
)


def parse_observation(text: str) -> tuple[str, list[dict]]:
    """Return (source, items) from one observation file, or raise ValueError.

    Each item: imdb_id; rating, an int 1-10 or None (IMDB showed it unrated);
    in_watchlist, a bool or None (not read); rated_on, an ISO date or ''."""
    data = json.loads(text)
    if not isinstance(data, dict) or data.get('version') != 1:
        raise ValueError('unknown version')
    items = []
    for raw in data.get('items') or []:
        imdb_id = raw.get('imdb_id', '')
        rating  = raw.get('rating')
        in_wl   = raw.get('in_watchlist')
        rated   = raw.get('rated_on') or ''
        if not IMDB_ONLY_RE.match(str(imdb_id)):
            raise ValueError(f'bad imdb_id {imdb_id!r}')
        if rating is not None and (not isinstance(rating, int) or isinstance(rating, bool) or not 1 <= rating <= 10):
            raise ValueError(f'bad rating {rating!r} for {imdb_id}')
        if in_wl is not None and not isinstance(in_wl, bool):
            raise ValueError(f'bad in_watchlist {in_wl!r} for {imdb_id}')
        if rated and not DATE_RE.match(rated):
            raise ValueError(f'bad rated_on {rated!r} for {imdb_id}')
        items.append({'imdb_id': imdb_id, 'rating': rating, 'in_watchlist': in_wl, 'rated_on': rated})
    return str(data.get('source', '')), items


def flag_unrated(vault: Path, imdb_id: str, title: str, local_rating: str, dry_run: bool) -> None:
    """IMDB shows no rating but the note has one: never guess which is right, ask.
    One open line per title; a second sighting adds nothing."""
    path = vault / '_actions' / 'actions.md'
    text = path.read_text(encoding='utf-8') if path.exists() else ''
    if any(imdb_id in l for l in text.splitlines() if l.lstrip().startswith('- [ ]')):
        return
    line = (f'- [ ] {title or imdb_id} ({imdb_id}): IMDB shows no rating, the vault has {local_rating}. '
            f'Check which is right. ➕ {date.today()}\n')
    print(f"  Flagged: {imdb_id} unrated on IMDB, {local_rating} in the vault")
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    text = text or ACTIONS_HEADER
    if not text.endswith('\n'):
        text += '\n'
    path.write_text(text + line, encoding='utf-8')


def apply_observation(vault: Path, item: dict, existing: dict, stats: dict, dry_run: bool) -> bool:
    """Apply one observed title. Returns False when it must be retried (OMDB unavailable).

    IMDB decides only my_rating and watchlist membership; following, last_season_watched
    and the rest are never written here."""
    imdb_id, rating, in_wl = item['imdb_id'], item['rating'], item['in_watchlist']
    note = existing.get(imdb_id)

    if note is None:
        if rating is not None:
            return create_note(imdb_id, str(rating), existing, stats, dry_run, item['rated_on']) is not False
        if in_wl:
            return create_note(imdb_id, '', existing, stats, dry_run) is not False
        return True  # a title you only looked at

    if rating is not None:
        apply_rating(note, imdb_id, str(rating), item['rated_on'] or str(date.today()), stats, dry_run)
        return True

    content = note.read_text(encoding='utf-8')
    fm, _ = vi.read_frontmatter(content)
    if fm.get('my_rating'):
        flag_unrated(vault, imdb_id, fm.get('title', ''), fm['my_rating'], dry_run)
        stats['flagged'] = stats.get('flagged', 0) + 1
        return True

    status = fm.get('status', '')
    new = 'to-watch' if (in_wl is True and status == 'removed') else \
          'removed'  if (in_wl is False and status == 'to-watch') else None
    if new:
        print(f"  Status {status} → {new}: {imdb_id}")
        if not dry_run:
            note.write_text(vi.update_field(content, 'status', new), encoding='utf-8')
        stats['updated'] += 1
    return True


def process_observations(vault: Path, existing: dict, stats: dict, dry_run: bool) -> None:
    """Apply every observation file in name order (the names start with the time seen).

    A file whose items all applied moves to processed/. One with items left to retry is
    rewritten to hold only those, so a later run never replays an older rating over a
    newer one. An unreadable file moves to failed/."""
    obs_dir = vault / OBS_SUBDIR
    if not obs_dir.is_dir():
        return
    files = sorted(obs_dir.glob('*.json'))
    if files:
        print(f"Observations: {len(files)} file{'' if len(files) == 1 else 's'}")
    for f in files:
        try:
            _, items = parse_observation(f.read_text(encoding='utf-8'))
        except (ValueError, OSError) as e:
            print(f"  Unreadable {f.name}: {e}", file=sys.stderr)
            stats['errors'] += 1
            if not dry_run:
                (obs_dir / 'failed').mkdir(exist_ok=True)
                f.replace(obs_dir / 'failed' / f.name)
            continue
        retry = []
        for item in items:
            try:
                if not apply_observation(vault, item, existing, stats, dry_run):
                    retry.append(item)
            except Exception as e:
                print(f"  Error {item['imdb_id']}: {e}", file=sys.stderr)
                stats['errors'] += 1
                retry.append(item)
        if dry_run:
            continue
        if retry:
            data = json.loads(f.read_text(encoding='utf-8'))
            data['items'] = [i for i in data['items'] if i.get('imdb_id') in {r['imdb_id'] for r in retry}]
            f.write_text(json.dumps(data), encoding='utf-8')
        else:
            (obs_dir / 'processed').mkdir(exist_ok=True)
            f.replace(obs_dir / 'processed' / f.name)

    done = obs_dir / 'processed'
    if done.is_dir() and not dry_run:
        cutoff = time.time() - OBS_KEEP_DAYS * 86400
        for old in done.glob('*.json'):
            if old.stat().st_mtime < cutoff:
                old.unlink()


# ---------------------------------------------------------------------------
# Queue pass
# ---------------------------------------------------------------------------

def process_queue(existing: dict, stats: dict, dry_run: bool) -> None:
    lines, content = read_queue(QUEUE_NOTE)
    if not lines:
        return

    print(f"Queue: {len(lines)} entr{'y' if len(lines) == 1 else 'ies'}")
    processed = []

    for line in lines:
        rated_match = RATING_LINE.match(line)
        if rated_match:
            url, rating_str = rated_match.group(1), rated_match.group(2)
            id_m = IMDB_ID_RE.search(url)
            if not id_m:
                print(f"  Skipping (no IMDB ID): {line}")
                continue
            imdb_id   = id_m.group(1)
            my_rating = str(int(float(rating_str)))
        else:
            id_m = IMDB_ID_RE.search(line)
            if not id_m:
                print(f"  Skipping (no IMDB ID): {line}")
                continue
            imdb_id   = id_m.group(1)
            my_rating = ''

        try:
            if imdb_id in existing:
                if not my_rating:
                    print(f"  Already exists: {imdb_id}")
                    stats['skipped'] += 1
                    processed.append(line)
                    continue

                apply_rating(existing[imdb_id], imdb_id, my_rating, str(date.today()), stats, dry_run)
                processed.append(line)

            else:
                if create_note(imdb_id, my_rating, existing, stats, dry_run):
                    processed.append(line)

        except Exception as e:
            print(f"  Error {imdb_id}: {e}", file=sys.stderr)
            stats['errors'] += 1

    if processed and not dry_run:
        archive_entries(QUEUE_NOTE, processed, content)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description='Process Watchlog queue.')
    p.add_argument('--dry-run', action='store_true', help='Report only — write no files')
    args = p.parse_args()

    vi.load_env(VAULT_ROOT)

    if args.dry_run:
        print('Dry run — no files will be written.')

    print('Scanning vault...')
    existing = vi.scan_vault(VAULT_ROOT)
    print(f'  Existing notes: {len(existing):,}')

    stats = {'added': 0, 'updated': 0, 'skipped': 0, 'errors': 0, 'flagged': 0}

    process_queue(existing, stats, args.dry_run)
    process_observations(VAULT_ROOT, existing, stats, args.dry_run)

    if stats['added'] or stats['updated'] or stats['errors'] or stats['flagged']:
        print(f"\nDone.")
        print(f"  Added:   {stats['added']}")
        print(f"  Updated: {stats['updated']}")
        print(f"  Skipped: {stats['skipped']}")
        if stats['flagged']:
            print(f"  Flagged: {stats['flagged']}")
        if stats['errors']:
            print(f"  Errors:  {stats['errors']}")
    else:
        print("Queue empty — nothing to do.")


if __name__ == '__main__':
    main()
