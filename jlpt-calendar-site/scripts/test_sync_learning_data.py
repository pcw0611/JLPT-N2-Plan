import io
import json
import unittest
from unittest.mock import patch
from sync_learning_data import sync_endpoints, sync_report, SYNC_ENDPOINTS


class SyncTests(unittest.TestCase):
    def test_default_targets_keep_cloudflare_and_legacy(self):
        self.assertEqual(sync_endpoints('both'), list(SYNC_ENDPOINTS.items()))

    def test_explicit_target_and_existing_override(self):
        self.assertEqual(sync_endpoints('legacy'), [('legacy', SYNC_ENDPOINTS['legacy'])])
        self.assertEqual(sync_endpoints('both', 'http://localhost/api/sync'), [('custom', 'http://localhost/api/sync')])

    def test_matching_origin_and_payload(self):
        with patch('urllib.request.urlopen', return_value=io.BytesIO(b'{"ok":true,"date":"2026-08-28"}')) as send:
            sync_report({'date': '2026-08-28'}, SYNC_ENDPOINTS['cloudflare'], 'test-only-secret')
        request = send.call_args.args[0]
        self.assertEqual(request.get_header('Origin'), 'https://jlpt-study-calendar.pcw0611.workers.dev')
        self.assertEqual(request.get_header('Authorization'), 'Bearer test-only-secret')
        self.assertEqual(json.loads(request.data)['date'], '2026-08-28')

    def test_wrong_date_is_not_reported_as_success(self):
        with patch('urllib.request.urlopen', return_value=io.BytesIO(b'{"ok":true,"date":"2026-08-27"}')):
            with self.assertRaises(RuntimeError):
                sync_report({'date': '2026-08-28'}, SYNC_ENDPOINTS['cloudflare'], 'test-only-secret')


if __name__ == '__main__':
    unittest.main()
