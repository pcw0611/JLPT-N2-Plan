import json
from pathlib import Path
import sqlite3
import unittest
from report_builder import make_report, TAXONOMY

DB = Path(__file__).resolve().parents[2] / 'database/jlpt_learning.db'


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        with sqlite3.connect(f'{DB.as_uri()}?mode=ro', uri=True) as src:
            src.backup(self.conn)

    def tearDown(self):
        self.conn.close()

    def report(self, date='2026-08-28'):
        return make_report(self.conn, date)

    def row(self, key, date='2026-08-28'):
        return next(r for r in self.report(date)['types'] if r['key']==key)

    def test_same_order_and_complete_taxonomy_all_days(self):
        for date in ('2026-08-26','2026-08-27','2026-08-28'):
            r=self.report(date)
            self.assertEqual([t['key'] for t in r['types']], [t['key'] for t in TAXONOMY['types']])
            self.assertEqual([d['key'] for d in r['domains']], [d['key'] for d in TAXONOMY['domains']])

    def test_unattempted_is_not_zero_over_cumulative(self):
        r=self.row('adjective_conjugation')
        self.assertEqual((r['correct'],r['total']),(0,0))
        self.assertGreater(r['cumulative']['total'],0)
        self.assertIsNone(r['averageSeconds'])

    def test_as_of_date_and_missing_snapshot(self):
        self.assertEqual(self.row('listening_task','2026-08-26')['cumulative']['total'],3)
        self.assertEqual(self.row('listening_task')['cumulative']['total'],10)
        self.assertEqual(self.row('kanji_reading','2026-08-26')['total'],7)

    def test_totals_preserved_missing_details_disclosed(self):
        for date,expected in [('2026-08-26',(58,43)),('2026-08-27',(47,32)),('2026-08-28',(32,20))]:
            r=self.report(date)
            self.assertEqual((r['tests']['total'],r['tests']['correct']),expected)
            detail=sum(t['total']+t['excluded'] for t in r['types'])
            self.assertEqual(detail+r['tests']['unclassifiedItems'],r['tests']['total'])
        self.assertEqual(self.report('2026-08-26')['tests']['unclassifiedItems'],12)
        self.assertEqual(self.report('2026-08-27')['tests']['unanswered'],2)

    def test_listening_decision_not_audio_or_total(self):
        r=self.row('listening_task')
        self.assertEqual(r['averageSeconds'],2.2)
        self.assertEqual(r['timedItems'],4)
        self.assertEqual(r['timingBasis'],'audio_end_to_answer')
        self.assertIsNone(self.row('listening_task','2026-08-27')['averageSeconds'])

    def test_null_notes_dont_exclude_valid_time(self):
        self.conn.execute("UPDATE tests SET notes=NULL WHERE id='2026-08-26-mixed-10'")
        self.assertIsNotNone(self.row('kanji_reading','2026-08-26')['averageSeconds'])

    def test_audio_error_excluded_and_disclosed(self):
        self.conn.execute("UPDATE tests SET notes=? WHERE id='n3-listening-order-time-20260828'",(json.dumps({'audio_error_items':[1]}),))
        r=self.row('listening_task')
        self.assertEqual((r['correct'],r['total'],r['excluded']),(1,3,1))
        self.assertEqual(self.report()['tests']['excludedItems'],1)
        self.assertEqual(self.report()['tests']['total'],32)

    def test_historical_review_does_not_use_future_sources_or_pending(self):
        before=self.report('2026-08-26')['nextReview']
        self.conn.execute("UPDATE review_queue SET status='completed'")
        self.assertEqual(self.report('2026-08-26')['nextReview'],before)
        self.assertEqual(before['date'],'2026-08-27')

    def test_missing_session_fails_closed(self):
        with self.assertRaises(ValueError):
            self.report('2026-08-01')

    def test_anki_stats_are_scoped_and_date_specific(self):
        anki = self.report('2026-08-30')['anki']
        self.assertEqual(anki['scope'], 'deck:current')
        self.assertEqual(anki['answeredCards'], 402)
        self.assertEqual(anki['forecast']['tomorrowDue'], 46)
        self.assertIsNone(self.report('2026-08-29')['anki'])


if __name__=='__main__':
    unittest.main()
