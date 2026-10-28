"""Tests for the userscript observation path in scripts/process_queues.py.

Assumptions pinned: observation files are version-1 JSON, {"version": 1, "source": ...,
"items": [{"imdb_id", "rating" (int or null), "in_watchlist" (bool), "rated_on"?}]},
as userscript/imdb-capture.js writes them. Notes are found by their imdb_id frontmatter
line. No network: the TVmaze and OMDB fetchers are stubbed, and sleeps are skipped.

Run: python3 -m unittest discover -s tests
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parent.parent / 'scripts' / 'process_queues.py'
spec = importlib.util.spec_from_file_location('process_queues', SCRIPT)
pq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pq)

MOVIE = '''---
title: {title}
imdb_id: {imdb_id}
my_rating: {rating}
type: movie
status: {status}
{extra}---
'''

SHOW = '''---
title: {title}
imdb_id: {imdb_id}
my_rating: {rating}
type: tv-series
status: {status}
series_status: {series}
following: true
last_season_watched: 2
---
'''


def omdb_ok(imdb_id):
    return {'found': True, 'title': f'Film {imdb_id}', 'year': '2026', 'omdb_type': 'movie'}


class ObservationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name)
        (self.vault / 'Movies').mkdir()
        (self.vault / 'TV Shows').mkdir()
        self.obs = self.vault / '_data' / 'imdb'
        self.obs.mkdir(parents=True)
        patches = [
            mock.patch.object(pq, 'VAULT_ROOT', self.vault),
            mock.patch.object(pq, 'tvmaze_quick_lookup', lambda i: None),
            mock.patch.object(pq, 'omdb_full_fetch', omdb_ok),
            mock.patch.object(pq.time, 'sleep', lambda s: None),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.tmp.cleanup)
        self.n = 0

    def movie(self, imdb_id, rating='', status='to-watch', extra=''):
        path = self.vault / 'Movies' / f'{imdb_id}.md'
        path.write_text(MOVIE.format(title=f'Movie {imdb_id}', imdb_id=imdb_id, rating=rating,
                                     status=status, extra=extra), encoding='utf-8')
        return path

    def show(self, imdb_id, rating='', status='to-watch', series='Running'):
        path = self.vault / 'TV Shows' / f'{imdb_id}.md'
        path.write_text(SHOW.format(title=f'Show {imdb_id}', imdb_id=imdb_id, rating=rating,
                                    status=status, series=series), encoding='utf-8')
        return path

    def observe(self, *items, source='title'):
        self.n += 1
        f = self.obs / f'2026-10-28T12-00-{self.n:02d}-000_{source}.json'
        f.write_text(json.dumps({'version': 1, 'source': source, 'seen_at': '2026-10-28T12:00:00',
                                 'items': list(items)}), encoding='utf-8')
        return f

    def run_processor(self):
        stats = {'added': 0, 'updated': 0, 'skipped': 0, 'errors': 0, 'flagged': 0}
        pq.process_observations(self.vault, pq.vi.scan_vault(self.vault), stats, dry_run=False)
        return stats

    def fm(self, path):
        return pq.vi.read_frontmatter(path.read_text(encoding='utf-8'))[0]

    # ---- rated ------------------------------------------------------------

    def test_rated_new_title_is_created_watched_with_rated_on(self):
        self.observe({'imdb_id': 'tt1', 'rating': 7, 'in_watchlist': False, 'rated_on': '2026-10-23'}, source='ratings')
        self.run_processor()
        notes = list((self.vault / 'Movies').glob('*.md'))
        self.assertEqual(len(notes), 1)
        fm = self.fm(notes[0])
        self.assertEqual((fm['my_rating'], fm['status'], fm['date_watched']), ('7', 'watched', '2026-10-23'))

    def test_changed_rating_updates_and_keeps_existing_date(self):
        note = self.movie('tt2', rating='6', status='watched', extra='date_watched: 2025-01-01\n')
        self.observe({'imdb_id': 'tt2', 'rating': 8, 'in_watchlist': False})
        self.run_processor()
        fm = self.fm(note)
        self.assertEqual((fm['my_rating'], fm['date_watched']), ('8', '2025-01-01'))

    def test_rated_running_show_follows_existing_tv_rule(self):
        high = self.show('tt3', series='Running')
        low = self.show('tt4', series='Running')
        self.observe({'imdb_id': 'tt3', 'rating': 7, 'in_watchlist': False},
                     {'imdb_id': 'tt4', 'rating': 5, 'in_watchlist': False})
        self.run_processor()
        self.assertEqual(self.fm(high)['status'], 'watching')
        self.assertEqual(self.fm(low)['status'], 'watched')

    # ---- watchlist --------------------------------------------------------

    def test_watchlisted_new_title_is_created_to_watch(self):
        self.observe({'imdb_id': 'tt5', 'rating': None, 'in_watchlist': True}, source='watchlist')
        self.run_processor()
        notes = list((self.vault / 'Movies').glob('*.md'))
        self.assertEqual([self.fm(n)['status'] for n in notes], ['to-watch'])

    def test_browsed_title_creates_nothing(self):
        self.observe({'imdb_id': 'tt6', 'rating': None, 'in_watchlist': False})
        self.run_processor()
        self.assertEqual(list((self.vault / 'Movies').glob('*.md')), [])

    def test_removal_and_readd(self):
        removed = self.movie('tt7', status='to-watch')
        readded = self.movie('tt8', status='removed')
        self.observe({'imdb_id': 'tt7', 'rating': None, 'in_watchlist': False},
                     {'imdb_id': 'tt8', 'rating': None, 'in_watchlist': True})
        self.run_processor()
        self.assertEqual(self.fm(removed)['status'], 'removed')
        self.assertEqual(self.fm(readded)['status'], 'to-watch')

    def test_watching_show_off_watchlist_is_untouched(self):
        note = self.show('tt9', status='watching')
        before = note.read_text(encoding='utf-8')
        self.observe({'imdb_id': 'tt9', 'rating': None, 'in_watchlist': False})
        self.run_processor()
        self.assertEqual(note.read_text(encoding='utf-8'), before)

    # ---- unrated on IMDB, rated locally -----------------------------------

    def test_unrated_on_imdb_flags_once_and_changes_nothing(self):
        note = self.movie('tt10', rating='9', status='watched')
        before = note.read_text(encoding='utf-8')
        self.observe({'imdb_id': 'tt10', 'rating': None, 'in_watchlist': False})
        self.run_processor()
        self.observe({'imdb_id': 'tt10', 'rating': None, 'in_watchlist': False})
        self.run_processor()
        self.assertEqual(note.read_text(encoding='utf-8'), before)
        actions = (self.vault / '_actions' / 'actions.md').read_text(encoding='utf-8')
        self.assertTrue(actions.startswith('# Actions\n'))
        self.assertEqual(sum('tt10' in l for l in actions.splitlines()), 1)

    # ---- files ------------------------------------------------------------

    def test_applied_file_moves_to_processed(self):
        f = self.observe({'imdb_id': 'tt11', 'rating': None, 'in_watchlist': False})
        self.run_processor()
        self.assertFalse(f.exists())
        self.assertTrue((self.obs / 'processed' / f.name).exists())

    def test_failed_creation_keeps_only_that_item(self):
        note = self.movie('tt12', rating='5', status='watched')
        f = self.observe({'imdb_id': 'tt12', 'rating': 6, 'in_watchlist': False},
                         {'imdb_id': 'tt13', 'rating': 8, 'in_watchlist': False})
        with mock.patch.object(pq, 'omdb_full_fetch', lambda i: {'found': False}):
            self.run_processor()
        self.assertEqual(self.fm(note)['my_rating'], '6')
        left = json.loads(f.read_text(encoding='utf-8'))['items']
        self.assertEqual([i['imdb_id'] for i in left], ['tt13'])
        self.run_processor()
        self.assertFalse(f.exists())

    def test_malformed_file_moves_to_failed(self):
        f = self.obs / '2026-10-28T12-00-00-000_title.json'
        f.write_text('{"version": 1, "items": [{"imdb_id": "nope"}]}', encoding='utf-8')
        stats = self.run_processor()
        self.assertEqual(stats['errors'], 1)
        self.assertTrue((self.obs / 'failed' / f.name).exists())


if __name__ == '__main__':
    unittest.main()
