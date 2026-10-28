"""Tests for scripts/tmdb_refresh.py: the availability rule, when a movie is due, and the
fields one run writes.

Assumptions pinned: TMDB's /movie/{id}/watch/providers returns {"results": {country:
{"flatrate"|"rent"|"buy"|"free"|"ads": [...], "link": ...}}} and /find returns
{"movie_results": [{"id", "release_date"}]}, as seen on 2026-10-28. No network: lookup()
is stubbed.

Run: python3 -m unittest discover -s tests
"""

import importlib.util
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parent.parent / 'scripts' / 'tmdb_refresh.py'
spec = importlib.util.spec_from_file_location('tmdb_refresh', SCRIPT)
tr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tr)

TODAY = date(2026, 10, 28)


def note(status='to-watch', extra='', released='2024-01-01', runtime='95', rating='7.5'):
    return (f'---\ntitle: Film\nimdb_id: tt1\nstatus: {status}\nreleased: {released}\n'
            f'runtime: {runtime}\nimdb_rating: {rating}\n{extra}---\n\nPlot.\n')


class RulesTest(unittest.TestCase):
    def test_available_any_kind_any_country(self):
        self.assertTrue(tr.available({'GR': {'link': 'x'}, 'US': {'rent': [{'provider_id': 2}]}}))
        self.assertTrue(tr.available({'DE': {'ads': [{}]}}))
        self.assertFalse(tr.available({'GR': {'link': 'x'}}))
        self.assertFalse(tr.available({}))

    def test_candidate_rules(self):
        # available: true keeps upcoming() out of it, so only the Easy watch rules decide.
        ok = {'released': '2024-01-01', 'runtime': '95', 'imdb_rating': '7.5', 'available': 'true'}
        self.assertTrue(tr.candidate(ok, TODAY))
        for change in ({'released': '2016-10-27'}, {'released': '2026-08-30'}, {'runtime': '101'},
                       {'imdb_rating': '6.9'}, {'released': ''}, {'runtime': ''}):
            self.assertFalse(tr.candidate({**ok, **change}, TODAY), change)

    def test_upcoming_is_a_candidate_until_available(self):
        long_new = {'released': '2026-07-17', 'runtime': '172', 'imdb_rating': '8.4', 'available': 'false'}
        self.assertTrue(tr.candidate(long_new, TODAY))
        self.assertTrue(tr.candidate({**long_new, 'released': '2026-12-01'}, TODAY))
        self.assertFalse(tr.candidate({**long_new, 'available': 'true'}, TODAY))
        self.assertFalse(tr.candidate({**long_new, 'released': '2024-01-01'}, TODAY))

    def test_due_ttls(self):
        self.assertTrue(tr.due({}, TODAY))
        self.assertTrue(tr.due({'tmdb_checked': '2026-10-21', 'available': 'false'}, TODAY))
        self.assertFalse(tr.due({'tmdb_checked': '2026-10-22', 'available': 'false'}, TODAY))
        self.assertFalse(tr.due({'tmdb_checked': '2026-10-21', 'available': 'true'}, TODAY))
        self.assertTrue(tr.due({'tmdb_checked': '2026-09-28', 'available': 'true'}, TODAY))


class RefreshTest(unittest.TestCase):
    def run_on(self, text, result):
        with tempfile.TemporaryDirectory() as root:
            vault = Path(root)
            (vault / 'Movies').mkdir()
            md = vault / 'Movies' / 'Film.md'
            md.write_text(text, encoding='utf-8')
            with mock.patch.object(tr, 'lookup', return_value=result):
                stats = tr.refresh(vault, 'k', dry_run=False, limit=None, today=TODAY)
            return stats, md.read_text(encoding='utf-8')

    def test_writes_only_tmdb_fields(self):
        stats, text = self.run_on(note(), ('603', '2023-12-25', True))
        fm = tr.vi.read_frontmatter(text)[0]
        self.assertEqual((fm['available'], fm['tmdb_id'], fm['tmdb_checked'], fm['released']),
                         ('true', '603', '2026-10-28', '2024-01-01'))
        self.assertTrue(text.endswith('---\n\nPlot.\n'))
        self.assertEqual(stats['available'], 1)

    def test_non_candidate_is_not_checked(self):
        stats, text = self.run_on(note(runtime='130'), ('603', '', True))
        self.assertNotIn('available', text)
        self.assertEqual(stats['checked'], 0)

    def test_skips_watched_and_not_due(self):
        stats, text = self.run_on(note(status='watched'), ('603', '', True))
        self.assertNotIn('available', text)
        stats, text = self.run_on(note(extra='tmdb_checked: 2026-10-27\navailable: false\n'), ('603', '', True))
        self.assertIn('available: false', text)
        self.assertEqual(stats['checked'], 0)

    def test_not_on_tmdb_still_records_the_check(self):
        stats, text = self.run_on(note(), None)
        self.assertIn('tmdb_checked: 2026-10-28', text)
        self.assertNotIn('available', text)
        self.assertEqual(stats['not_found'], 1)


if __name__ == '__main__':
    unittest.main()
