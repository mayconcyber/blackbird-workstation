import subprocess
import unittest
from unittest.mock import patch
from blackbird.network import collect_snapshot, decode_snapshot, filter_tcp


class NetworkTests(unittest.TestCase):
    def test_empty_and_bom(self):
        data = decode_snapshot('\ufeff{"interfaces": [], "tcp": []}')
        self.assertEqual(data['tcp'], [])
        self.assertIn('captured_at', data)

    def test_invalid_shape(self):
        for raw in ('[]', '{}', '{"interfaces": null, "tcp": []}', '{"interfaces": [], "tcp": [1]}'):
            with self.assertRaises(ValueError):
                decode_snapshot(raw)

    def test_filter_pid_ipv6_and_case(self):
        rows = [{'pid': 123, 'process': 'Python', 'local_address': '::1'}, {'pid': 456}]
        for query in ('123', 'PYTHON', '::1'):
            self.assertEqual(filter_tcp(rows, query), rows[:1])
        self.assertEqual(filter_tcp(rows, ''), rows)

    @patch('blackbird.network.subprocess.run')
    def test_timeout(self, run):
        run.side_effect = subprocess.TimeoutExpired('powershell', 30)
        with self.assertRaisesRegex(RuntimeError, '30 segundos'):
            collect_snapshot()

    @patch('blackbird.network.subprocess.run')
    def test_failed_query(self, run):
        run.return_value = subprocess.CompletedProcess([], 1, '', 'Access denied')
        with self.assertRaisesRegex(RuntimeError, 'Access denied'):
            collect_snapshot()

    @patch('blackbird.network.subprocess.run')
    def test_command_is_fixed_and_hidden(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, '{"interfaces": [], "tcp": []}', '')
        collect_snapshot()
        args, kwargs = run.call_args
        self.assertEqual(args[0][0], 'powershell.exe')
        self.assertEqual(kwargs['timeout'], 30)
        self.assertNotIn('shell', kwargs)
