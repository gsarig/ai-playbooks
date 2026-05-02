#!/usr/bin/env python3
"""
Watchlog import script.

Usage:
    python3 scripts/import.py --ratings <csv> --watchlist <csv> [--tvmaze] [--omdb] [--ttl-days N]

On each run:
- New entries are created as notes.
- Existing notes are updated only when my_rating, status, or imdb_rating changed.
- TV shows are queried on TVmaze only when series_status != Ended and the
  last check is older than --ttl-days (default 30), or when new fields are missing.
- Movies are queried on OMDB when omdb_last_checked is not set (first run only).
- Run stats are appended to .import-state.json (gitignored).
"""

import argparse
import csv
import html as _html
import json
import os
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

VAULT_ROOT = Path(__file__).resolve().parent.parent

# IMDB Title Type → (folder, type value)
# None means skip entirely; ("TV Shows", None) means Standout Episodes
TYPE_MAP = {
    "Movie":          ("Movies",   "movie"),
    "TV Movie":       ("Movies",   "tv-movie"),
    "Short":          ("Movies",   "short"),
    "Video":          ("Movies",   "video"),
    "TV Series":      ("TV Shows", "tv-series"),
    "TV Mini Series": ("TV Shows", "tv-miniseries"),
    "TV Episode":     ("TV Shows", None),
    "Podcast Series": None,
}

TVMAZE_RATE = 0.55   # seconds between requests (~20 req/10 s)
OMDB_RATE   = 0.5    # seconds between requests
DEFAULT_TTL  = 30    # days before re-checking ongoing shows


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

def load_env(vault: Path) -> None:
    env_path = vault / '.env'
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, _, v = line.partition('=')
        os.environ.setdefault(k.strip(), v.strip())


# ---------------------------------------------------------------------------
# Filename helpers
# ---------------------------------------------------------------------------

_INVALID_WIN = re.compile(r'[<>:"/\\|?*]')
_MULTI_SPACE  = re.compile(r'\s+')

def safe_filename(title: str, year: str) -> str:
    title = _INVALID_WIN.sub('', title)
    title = _MULTI_SPACE.sub(' ', title).strip()
    return f"{title} ({year}).md"


# ---------------------------------------------------------------------------
# YAML frontmatter — minimal but correct formatter
# ---------------------------------------------------------------------------

def _yaml_value(v) -> str:
    if v is None or v == '':
        return ''
    if isinstance(v, list):
        return '[' + ', '.join(str(i) for i in v) + ']' if v else '[]'
    s = str(v)
    if any(c in s for c in ':#{}[]|>&*!,\'') or s != s.strip():
        s = s.replace('"', '\\"')
        return f'"{s}"'
    return s

def format_frontmatter(fields: list) -> str:
    """fields: list of (key, value) tuples — order is preserved."""
    lines = ['---']
    for k, v in fields:
        lines.append(f'{k}: {_yaml_value(v)}')
    lines.append('---')
    return '\n'.join(lines)

FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n?', re.DOTALL)

def read_frontmatter(content: str) -> tuple[dict, str]:
    """Return (key→value dict, body text)."""
    m = FRONTMATTER_RE.match(content)
    if not m:
        return {}, content
    body = content[m.end():]
    fm: dict = {}
    for line in m.group(1).splitlines():
        if ':' not in line:
            continue
        k, _, raw = line.partition(':')
        k = k.strip()
        raw = raw.strip()
        if raw.startswith('[') and raw.endswith(']'):
            fm[k] = [x.strip().strip('"\'') for x in raw[1:-1].split(',') if x.strip()]
        else:
            fm[k] = raw.strip('"\'')
    return fm, body

def update_field(content: str, key: str, value) -> str:
    """Replace a single frontmatter field in-place."""
    pattern = re.compile(rf'^({re.escape(key)}:[^\S\n]*).*$', re.MULTILINE)
    replacement = rf'\g<1>{_yaml_value(value)}'
    new, count = pattern.subn(replacement, content, count=1)
    if count == 0:
        # Field missing — insert before closing --- (first \n--- not at position 0)
        new = re.sub(r'\n---\n', f'\n{key}: {_yaml_value(value)}\n---\n', new, count=1)
    return new


# ---------------------------------------------------------------------------
# CSV parsing
# ---------------------------------------------------------------------------

def parse_csv(path: str) -> list[dict]:
    rows = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            tt = row.get('Title Type', '').strip()
            if not tt or tt.startswith('http'):
                continue
            rows.append(row)
    return rows

def build_lookup(rows: list[dict]) -> dict[str, dict]:
    return {r['Const'].strip(): r for r in rows if r.get('Const', '').startswith('tt')}

def parse_list(s: str) -> list[str]:
    return [x.strip() for x in s.split(',') if x.strip()] if s else []


# ---------------------------------------------------------------------------
# Status logic
# ---------------------------------------------------------------------------

def determine_status(wl: dict | None, rt: dict | None) -> tuple[str, str]:
    """Returns (status, date_watched). No personal rating means not watched yet.
    Final status for TV shows is resolved later once series_status is known."""
    rating = ''
    if rt:
        rating = rt.get('Your Rating', '').strip()
    if not rating and wl:
        rating = wl.get('Your Rating', '').strip()

    date_w = ''
    if rt:
        date_w = rt.get('Date Rated', '').strip()
    if not date_w and wl:
        date_w = wl.get('Date Rated', '').strip()

    if not rating:
        return 'to-watch', ''
    return 'watched', date_w


def resolve_tv_status(status: str, series_status: str, my_rating: str) -> str:
    """Apply TV-specific status rules once series_status is known."""
    if not my_rating:
        return 'to-watch'
    try:
        r = int(float(my_rating))
    except (ValueError, TypeError):
        return status
    if series_status == 'Ended' or r < 6:
        return 'watched'
    return 'watching'


# ---------------------------------------------------------------------------
# Vault scanner
# ---------------------------------------------------------------------------

def scan_vault(vault: Path) -> dict[str, Path]:
    """Return {imdb_id: note_path} for all existing notes."""
    result: dict[str, Path] = {}
    for md in vault.rglob('*.md'):
        try:
            text = md.read_text(encoding='utf-8')
            m = re.search(r'^imdb_id:\s*(tt\d+)', text, re.MULTILINE)
            if m:
                result[m.group(1)] = md
        except OSError:
            pass
    return result


# ---------------------------------------------------------------------------
# TVmaze
# ---------------------------------------------------------------------------

def _strip_html(s: str) -> str:
    return _html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()


def tvmaze_fetch(imdb_id: str, title: str, tvmaze_id: int | None = None) -> dict:
    """Return dict with tvmaze fields including new metadata and summary."""
    result = {
        'tvmaze_id':           '',
        'total_seasons':       '',
        'series_status':       '',
        'next_season_start':   '',
        'next_season_date':    '',
        'tvmaze_last_checked': str(date.today()),
        'language':            '',
        'network':             '',
        'country':             '',
        'show_type':           '',
        'premiered':           '',
        'ended':               '',
        'summary':             '',
    }
    if not HAS_REQUESTS:
        return result

    try:
        if tvmaze_id:
            r = requests.get(f'https://api.tvmaze.com/shows/{tvmaze_id}', timeout=10)
        else:
            r = requests.get(
                f'https://api.tvmaze.com/lookup/shows?imdb={imdb_id}',
                timeout=10,
            )
            if r.status_code == 404:
                r = requests.get(
                    f'https://api.tvmaze.com/singlesearch/shows?q={requests.utils.quote(title)}',
                    timeout=10,
                )
        if r.status_code != 200:
            return result

        show = r.json()
        result['tvmaze_id']     = str(show['id'])
        result['series_status'] = show.get('status', '')
        result['language']      = show.get('language', '') or ''
        result['show_type']     = show.get('type', '') or ''
        result['premiered']     = show.get('premiered', '') or ''
        result['ended']         = show.get('ended', '') or ''
        network = show.get('network') or {}
        result['network']       = network.get('name', '') or ''
        result['country']       = (network.get('country') or {}).get('code', '') or ''
        result['summary']       = _strip_html(show.get('summary', ''))

        # Always fetch seasons to get total_seasons count
        time.sleep(TVMAZE_RATE)
        seasons_r = requests.get(
            f'https://api.tvmaze.com/shows/{show["id"]}/seasons',
            timeout=10,
        )
        if seasons_r.status_code != 200:
            return result

        seasons = seasons_r.json()
        result['total_seasons'] = str(len(seasons))

        if show.get('status') == 'Ended':
            return result

        today = str(date.today())

        # Upcoming = premiere in the future OR no end date yet
        upcoming = [
            s for s in seasons
            if (s.get('endDate') and s['endDate'] >= today)
            or (s.get('premiereDate') and s['premiereDate'] >= today)
            or (s.get('premiereDate') and not s.get('endDate'))
        ]
        if not upcoming:
            return result

        next_s = min(upcoming, key=lambda s: s.get('premiereDate') or '9999-99-99')
        result['next_season_start'] = next_s.get('premiereDate', '')
        end = next_s.get('endDate')
        if end:
            result['next_season_date'] = end
            return result

        # endDate missing — get episodes and take the latest airdate
        time.sleep(TVMAZE_RATE)
        eps_r = requests.get(
            f'https://api.tvmaze.com/shows/{show["id"]}/episodes?specials=0',
            timeout=10,
        )
        if eps_r.status_code == 200:
            eps = [
                e for e in eps_r.json()
                if e.get('season') == next_s['number'] and e.get('airdate')
            ]
            if eps:
                result['next_season_date'] = max(e['airdate'] for e in eps)

    except Exception as e:
        print(f"    TVmaze error ({imdb_id}): {e}", file=sys.stderr)

    return result


def infer_following(series_status: str, my_rating: str) -> str:
    """Return 'true' if rated 6+, 'false' if ended or rated below 6, else ''."""
    if series_status == 'Ended':
        return 'false'
    try:
        if my_rating:
            return 'true' if int(float(my_rating)) >= 6 else 'false'
    except (ValueError, TypeError):
        pass
    return ''


def needs_tvmaze(fm: dict, ttl: int) -> bool:
    if not fm.get('tvmaze_id'):
        return True
    if not fm.get('language'):  # backfill new metadata fields for existing notes
        return True
    if not fm.get('poster'):    # backfill poster for existing notes
        return True
    if fm.get('series_status') == 'Ended':
        return False
    last = fm.get('tvmaze_last_checked', '')
    if not last:
        return True
    try:
        return (date.today() - date.fromisoformat(last)).days >= ttl
    except ValueError:
        return True


# ---------------------------------------------------------------------------
# OMDB
# ---------------------------------------------------------------------------

def omdb_fetch(imdb_id: str) -> dict:
    """Return dict with OMDB metadata fields and plot."""
    result = {
        'language':          '',
        'country':           '',
        'rated':             '',
        'metascore':         '',
        'awards':            '',
        'writer':            '',
        'actors':            '',
        'poster':            '',
        'plot':              '',
        'omdb_last_checked': str(date.today()),
    }
    api_key = os.environ.get('OMDB_API_KEY', '')
    if not api_key or not HAS_REQUESTS:
        return result
    try:
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
        for key, omdb_key in [
            ('language',  'Language'),
            ('country',   'Country'),
            ('rated',     'Rated'),
            ('metascore', 'Metascore'),
            ('awards',    'Awards'),
            ('writer',    'Writer'),
            ('actors',    'Actors'),
            ('poster',    'Poster'),
            ('plot',      'Plot'),
        ]:
            val = data.get(omdb_key, '')
            result[key] = '' if val == 'N/A' else val
    except Exception as e:
        print(f"    OMDB error ({imdb_id}): {e}", file=sys.stderr)
    return result


def needs_omdb(fm: dict) -> bool:
    return not fm.get('omdb_last_checked')


# ---------------------------------------------------------------------------
# Note builders
# ---------------------------------------------------------------------------

def movie_fields(imdb_id, row_rt, row_wl, status, date_w) -> list:
    row = row_rt or row_wl
    _, type_val = TYPE_MAP.get(row.get('Title Type', '').strip(), ('Movies', 'movie'))
    rating = ''
    if row_rt:
        rating = row_rt.get('Your Rating', '').strip()
    if not rating and row_wl:
        rating = row_wl.get('Your Rating', '').strip()

    fields = [
        ('title',            row.get('Title', '').strip()),
        ('original_title',   row.get('Original Title', '').strip() or row.get('Title', '').strip()),
        ('imdb_id',          imdb_id),
        ('imdb_url',         f'https://www.imdb.com/title/{imdb_id}/'),
        ('imdb_rating',      row.get('IMDb Rating', '').strip()),
        ('my_rating',        rating),
        ('year',             row.get('Year', '').strip()),
        ('type',             type_val),
        ('genres',           parse_list(row.get('Genres', ''))),
        ('directors',        parse_list(row.get('Directors', ''))),
        ('runtime',          row.get('Runtime (mins)', '').strip()),
        ('status',           status),
        ('language',         ''),
        ('country',          ''),
        ('rated',            ''),
        ('metascore',        ''),
        ('awards',           ''),
        ('writer',           ''),
        ('actors',           ''),
        ('poster',           ''),
        ('omdb_last_checked', ''),
    ]
    if date_w:
        fields.append(('date_watched', date_w))
    return fields


def tv_fields(imdb_id, row_rt, row_wl, status, date_w) -> list:
    row = row_rt or row_wl
    _, type_val = TYPE_MAP.get(row.get('Title Type', '').strip(), ('TV Shows', 'tv-series'))
    rating = ''
    if row_rt:
        rating = row_rt.get('Your Rating', '').strip()
    if not rating and row_wl:
        rating = row_wl.get('Your Rating', '').strip()

    fields = [
        ('title',                row.get('Title', '').strip()),
        ('original_title',       row.get('Original Title', '').strip() or row.get('Title', '').strip()),
        ('imdb_id',              imdb_id),
        ('imdb_url',             f'https://www.imdb.com/title/{imdb_id}/'),
        ('imdb_rating',          row.get('IMDb Rating', '').strip()),
        ('my_rating',            rating),
        ('year',                 row.get('Year', '').strip()),
        ('type',                 type_val),
        ('genres',               parse_list(row.get('Genres', ''))),
        ('runtime',              row.get('Runtime (mins)', '').strip()),
        ('status',               status),
        ('tvmaze_id',            ''),
        ('total_seasons',        ''),
        ('series_status',        ''),
        ('following',            ''),
        ('current_season',       ''),
        ('last_season_watched',  ''),
        ('next_season_start',    ''),
        ('next_season_date',     ''),
        ('tvmaze_last_checked',  ''),
        ('language',             ''),
        ('network',              ''),
        ('country',              ''),
        ('show_type',            ''),
        ('premiered',            ''),
        ('ended',                ''),
    ]
    if date_w:
        fields.insert(fields.index(('series_status', '')), ('date_watched', date_w))
    return fields


TV_SEASON_TABLE = "| Season | Last episode | Watched |\n| --- | --- | --- |\n"


# ---------------------------------------------------------------------------
# Core processing
# ---------------------------------------------------------------------------

def process(
    imdb_id: str,
    row_wl: dict | None,
    row_rt: dict | None,
    vault: Path,
    existing: dict[str, Path],
    use_tvmaze: bool,
    use_omdb: bool,
    ttl: int,
    standout: list,
    stats: dict,
    dry_run: bool = False,
) -> None:
    row = row_rt or row_wl
    imdb_type = row.get('Title Type', '').strip()

    mapping = TYPE_MAP.get(imdb_type)
    if mapping is None:
        stats['skipped'] += 1
        return

    folder, type_val = mapping
    if type_val is None:                    # TV Episode → standout list
        standout.append(row)
        return

    is_tv   = folder == 'TV Shows'
    title   = row.get('Title', '').strip()
    year    = row.get('Year', '').strip()
    status, date_w = determine_status(row_wl, row_rt)

    existing_path = existing.get(imdb_id)

    if existing_path and existing_path.exists():
        # ---- update existing note -------------------------------------------
        content = existing_path.read_text(encoding='utf-8')
        fm, _ = read_frontmatter(content)

        changed = False
        updates: dict = {}

        # Fields driven by IMDB re-exports
        new_rating = ''
        if row_rt:
            new_rating = row_rt.get('Your Rating', '').strip()
        if not new_rating and row_wl:
            new_rating = row_wl.get('Your Rating', '').strip()

        for key, new_val in [
            ('status',       status),
            ('my_rating',    new_rating),
            ('imdb_rating',  row.get('IMDb Rating', '').strip()),
        ]:
            if str(fm.get(key, '')) != str(new_val):
                updates[key] = new_val
                changed = True

        if date_w and str(fm.get('date_watched', '')) != date_w:
            updates['date_watched'] = date_w
            changed = True

        # TVmaze refresh
        tvmaze_result = {}
        if is_tv and use_tvmaze and needs_tvmaze(fm, ttl):
            print(f"    TVmaze: {title}")
            stored_id = int(fm['tvmaze_id']) if fm.get('tvmaze_id') else None
            tvmaze_result = tvmaze_fetch(imdb_id, title, tvmaze_id=stored_id)
            time.sleep(TVMAZE_RATE)
            stats['tvmaze_calls'] += 1
            for k, v in tvmaze_result.items():
                if k == 'summary':
                    continue
                if k not in fm or str(fm.get(k, '')) != str(v):
                    updates[k] = v
                    changed = True

        # OMDB enrichment (movies only)
        omdb_result = {}
        if not is_tv and use_omdb and needs_omdb(fm):
            print(f"    OMDB: {title}")
            omdb_result = omdb_fetch(imdb_id)
            time.sleep(OMDB_RATE)
            stats['omdb_calls'] += 1
            for k, v in omdb_result.items():
                if k == 'plot':
                    continue
                if v and str(fm.get(k, '')) != str(v):
                    updates[k] = v
                    changed = True

        # Check whether body needs updating
        _, cur_body = read_frontmatter(content)
        needs_body_update = False
        if is_tv and tvmaze_result.get('summary') and cur_body.strip() == TV_SEASON_TABLE.strip():
            needs_body_update = True
            changed = True
        if not is_tv and omdb_result.get('plot') and not cur_body.strip():
            needs_body_update = True
            changed = True

        # Re-resolve TV status whenever we have series_status and a rating
        if is_tv:
            effective_series_status = updates.get('series_status', fm.get('series_status', ''))
            effective_rating = updates.get('my_rating', fm.get('my_rating', ''))
            current_status = updates.get('status', fm.get('status', ''))
            if effective_series_status and effective_rating:
                resolved = resolve_tv_status(current_status, effective_series_status, effective_rating)
                if resolved != current_status:
                    updates['status'] = resolved
                    changed = True

        # Auto-set following if not yet decided
        if is_tv and not fm.get('following') and 'following' not in updates:
            effective_status = updates.get('series_status', fm.get('series_status', ''))
            effective_rating = updates.get('my_rating', fm.get('my_rating', ''))
            inferred = infer_following(effective_status, effective_rating)
            if inferred:
                updates['following'] = inferred
                changed = True

        if changed:
            if not dry_run:
                for k, v in updates.items():
                    content = update_field(content, k, v)
                if needs_body_update:
                    fm_match = FRONTMATTER_RE.match(content)
                    if fm_match:
                        if is_tv:
                            content = (
                                content[:fm_match.end()]
                                + '\n' + tvmaze_result['summary'] + '\n\n'
                                + TV_SEASON_TABLE
                            )
                        else:
                            content = content[:fm_match.end()] + '\n' + omdb_result['plot'] + '\n'
                existing_path.write_text(content, encoding='utf-8')
            stats['updated'] += 1
        else:
            stats['skipped'] += 1

    else:
        # ---- create new note ------------------------------------------------
        if not dry_run:
            dest_dir = vault / folder
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / safe_filename(title, year)

            # Avoid clobbering a file that has a different imdb_id
            if dest.exists():
                dest = dest_dir / safe_filename(f"{title} [{imdb_id}]", year)

            if is_tv:
                fields = tv_fields(imdb_id, row_rt, row_wl, status, date_w)
                tvmaze_summary = ''
                if use_tvmaze:
                    print(f"    TVmaze: {title}")
                    tvmaze = tvmaze_fetch(imdb_id, title)
                    time.sleep(TVMAZE_RATE)
                    stats['tvmaze_calls'] += 1
                    tvmaze_keys = {
                        'tvmaze_id', 'total_seasons', 'series_status',
                        'next_season_start', 'next_season_date', 'tvmaze_last_checked',
                        'language', 'network', 'country', 'show_type', 'premiered', 'ended',
                    }
                    fields = [(k, tvmaze.get(k, v) if k in tvmaze_keys and tvmaze.get(k) else v)
                              for k, v in fields]
                    tvmaze_summary = tvmaze.get('summary', '')
                # Resolve TV status based on series_status and rating
                fields_dict = dict(fields)
                resolved = resolve_tv_status(
                    fields_dict.get('status', ''),
                    fields_dict.get('series_status', ''),
                    fields_dict.get('my_rating', ''),
                )
                fields = [(k, resolved if k == 'status' else v) for k, v in fields]
                # Auto-set following based on series status and rating
                fields_dict = dict(fields)
                inferred = infer_following(fields_dict.get('series_status', ''), fields_dict.get('my_rating', ''))
                if inferred:
                    fields = [(k, inferred if k == 'following' else v) for k, v in fields]
                if tvmaze_summary:
                    body = '\n\n' + tvmaze_summary + '\n\n' + TV_SEASON_TABLE
                else:
                    body = '\n\n' + TV_SEASON_TABLE
                content = format_frontmatter(fields) + body
            else:
                fields = movie_fields(imdb_id, row_rt, row_wl, status, date_w)
                omdb_plot = ''
                if use_omdb:
                    print(f"    OMDB: {title}")
                    omdb = omdb_fetch(imdb_id)
                    time.sleep(OMDB_RATE)
                    stats['omdb_calls'] += 1
                    omdb_keys = {
                        'language', 'country', 'rated', 'metascore',
                        'awards', 'writer', 'actors', 'poster', 'omdb_last_checked',
                    }
                    fields = [(k, omdb.get(k, v) if k in omdb_keys and omdb.get(k) else v)
                              for k, v in fields]
                    omdb_plot = omdb.get('plot', '')
                content = format_frontmatter(fields) + '\n'
                if omdb_plot:
                    content += '\n' + omdb_plot + '\n'

            dest.write_text(content, encoding='utf-8')
            existing[imdb_id] = dest
        stats['added'] += 1


def write_standout(episodes: list, vault: Path) -> None:
    if not episodes:
        return
    dest = vault / 'TV Shows' / '_Standout Episodes.md'
    existing_ids: set[str] = set()
    header = '# Standout Episodes\n\n'
    existing_body = ''
    if dest.exists():
        text = dest.read_text(encoding='utf-8')
        existing_ids = set(re.findall(r'tt\d+', text))
        existing_body = text if text.startswith('#') else header + text

    new_lines = []
    for row in episodes:
        iid = row.get('Const', '').strip()
        if iid in existing_ids:
            continue
        title    = row.get('Title', '').strip()
        year     = row.get('Year', '').strip()
        url      = row.get('URL', '').strip()
        rating   = row.get('Your Rating', '').strip()
        suffix   = f' · {rating}/10' if rating else ''
        new_lines.append(f'- [{title} ({year})]({url}){suffix} `{iid}`')

    if not new_lines:
        return

    if existing_body:
        text = existing_body.rstrip('\n') + '\n' + '\n'.join(new_lines) + '\n'
    else:
        text = header + '\n'.join(new_lines) + '\n'

    dest.write_text(text, encoding='utf-8')
    print(f'  Standout Episodes: +{len(new_lines)} entries')


def save_state(stats: dict, vault: Path) -> None:
    path = vault / '.import-state.json'
    runs = []
    if path.exists():
        try:
            runs = json.loads(path.read_text()).get('runs', [])
        except Exception:
            pass
    runs.append({'timestamp': datetime.now().isoformat(timespec='seconds'), **stats})
    path.write_text(json.dumps({'runs': runs}, indent=2))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description='Import IMDB exports into Watchlog.')
    p.add_argument('--ratings',   default=None, help='IMDB ratings CSV (default: imports/ratings.csv)')
    p.add_argument('--watchlist', default=None, help='IMDB watchlist CSV (default: imports/watchlist.csv)')
    p.add_argument('--vault',     default=str(VAULT_ROOT), help='Vault root (default: repo root)')
    p.add_argument('--tvmaze',    action='store_true', help='Fetch TVmaze data for TV shows')
    p.add_argument('--omdb',      action='store_true', help='Fetch OMDB data for movies (requires OMDB_API_KEY in .env)')
    p.add_argument('--dry-run',   action='store_true', help='Parse and report only — write no files, make no API calls')
    p.add_argument('--limit',     type=int, default=None, help='Process only the first N entries (for testing)')
    p.add_argument('--ttl-days',  type=int, default=DEFAULT_TTL,
                   help=f'Days before re-checking ongoing shows (default {DEFAULT_TTL})')
    args = p.parse_args()

    if args.tvmaze and not HAS_REQUESTS:
        sys.exit('Error: --tvmaze requires the requests library. pip install requests')
    if args.omdb and not HAS_REQUESTS:
        sys.exit('Error: --omdb requires the requests library. pip install requests')

    if args.dry_run:
        print('Dry run — no files will be written, no API calls will be made.')

    vault = Path(args.vault)
    load_env(vault)

    if args.omdb and not os.environ.get('OMDB_API_KEY'):
        sys.exit('Error: --omdb requires OMDB_API_KEY in .env')

    ratings_path   = args.ratings   or str(vault / 'imports' / 'ratings.csv')
    watchlist_path = args.watchlist or str(vault / 'imports' / 'watchlist.csv')

    for path, label in [(ratings_path, 'ratings'), (watchlist_path, 'watchlist')]:
        if not Path(path).exists():
            sys.exit(f'Error: {label} CSV not found at {path}')

    print('Parsing CSVs...')
    rt_rows = parse_csv(ratings_path)
    wl_rows = parse_csv(watchlist_path)
    rt_map  = build_lookup(rt_rows)
    wl_map  = build_lookup(wl_rows)
    print(f'  Ratings:   {len(rt_map):,}')
    print(f'  Watchlist: {len(wl_map):,}')

    print('Scanning vault...')
    existing = scan_vault(vault)
    print(f'  Existing notes: {len(existing):,}')

    all_ids = sorted(set(rt_map) | set(wl_map))
    if args.limit:
        all_ids = all_ids[:args.limit]
        print(f'Processing {len(all_ids)} entries (--limit {args.limit})...')
    else:
        print(f'Processing {len(all_ids):,} unique entries...')

    stats    = {'added': 0, 'updated': 0, 'skipped': 0, 'tvmaze_calls': 0, 'omdb_calls': 0, 'errors': 0}
    standout = []

    for i, iid in enumerate(all_ids, 1):
        if i % 200 == 0:
            print(f'  {i:,}/{len(all_ids):,}')
        try:
            process(
                imdb_id    = iid,
                row_wl     = wl_map.get(iid),
                row_rt     = rt_map.get(iid),
                vault      = vault,
                existing   = existing,
                use_tvmaze = args.tvmaze and not args.dry_run,
                use_omdb   = args.omdb and not args.dry_run,
                ttl        = args.ttl_days,
                standout   = standout,
                stats      = stats,
                dry_run    = args.dry_run,
            )
        except Exception as e:
            print(f'  Error {iid}: {e}', file=sys.stderr)
            stats['errors'] += 1

    if not args.dry_run:
        write_standout(standout, vault)
        save_state(stats, vault)

    print(f'\n{"Dry run complete" if args.dry_run else "Done"} — no files written.' if args.dry_run else '\nDone.')
    print(f'  Added:        {stats["added"]:,}')
    print(f'  Updated:      {stats["updated"]:,}')
    print(f'  Skipped:      {stats["skipped"]:,}')
    if stats['tvmaze_calls']:
        print(f'  TVmaze calls: {stats["tvmaze_calls"]:,}')
    if stats['omdb_calls']:
        print(f'  OMDB calls:   {stats["omdb_calls"]:,}')
    if stats['errors']:
        print(f'  Errors:       {stats["errors"]:,}')


if __name__ == '__main__':
    main()
