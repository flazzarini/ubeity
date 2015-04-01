from ubiety.pinger import Pinger
from unittest import TestCase
from unittest.mock import patch


class TestPinger(TestCase):
    def setUp(self):
        self.name = "PingerTest"
        self.ip = "1.1.1.1"
        self.online = False
        self.delay = 20
        self.wait = 2
        self.pinger = Pinger(
            self.name,
            self.ip,
            online=self.online,
            delay=self.delay,
            wait=self.wait
        )

    def test_repr(self):
        expected = (
            "Pinger('{}', '{}', online={}, delay={}, wait={})"
            .format(
                self.name,
                self.ip,
                self.online,
                self.delay,
                self.wait
            )
        )
        self.assertEqual(str(self.pinger), expected)

    def test_set_online_true_whenfalse(self):
        expected = True
        result = self.pinger.set_online(True)
        self.assertEqual(result, expected)

    def test_set_online_true_whentrue(self):
        # Force pinger.online to True to trigger the if clauses in
        # ``set_online``
        self.pinger.online = True

        expected = True
        result = self.pinger.set_online(True)
        self.assertEqual(result, expected)

    def test_set_online_false_whenfalse(self):
        expected = False
        result = self.pinger.set_online(False)
        self.assertEqual(result, expected)

    def test_set_online_false_whentrue(self):
        # Force pinger.online to True to trigger the if clauses in
        # ``set_online``
        self.pinger.online = True

        expected = False
        result = self.pinger.set_online(False)
        self.assertEqual(result, expected)

    def test_set_online_raises(self):
        with self.assertRaises(ValueError):
            self.pinger.set_online(None)

    @patch('ubiety.pinger.call')
    def test_run_online(self, call_mock):
        call_mock.return_value = 0
        self.pinger.run(single_run=True)
        self.assertTrue(self.pinger.online)

    @patch('ubiety.pinger.call')
    def test_run_offline_but_not_set(self, call_mock):
        """
        Pinger in online status should only go offline after the thrid time
        the host is not reachable
        """
        call_mock.return_value = 1

        # Reset pinger retry and online status to True
        self.pinger.retry = 0
        self.pinger.online = True

        self.pinger.run(single_run=True)
        self.assertTrue(self.pinger.online)

    @patch('ubiety.pinger.call')
    def test_run_offline(self, call_mock):
        """
        Pinger in online status should only go offline after the thrid time
        the host is not reachable
        """
        call_mock.return_value = 1

        # Reset pinger retry and online status to True
        self.pinger.retry = 2
        self.pinger.online = True

        self.pinger.run(single_run=True)
        self.assertFalse(self.pinger.online)

    @patch('ubiety.pinger.call')
    def test_run_offline_increment_retry(self, call_mock):
        """
        If Pinger doesn't reach the host increase the retry count
        """
        call_mock.return_value = 1

        # Reset pinger retry and online status to True
        self.pinger.retry = 0
        self.pinger.online = True

        self.pinger.run(single_run=True)
        self.assertEqual(self.pinger.retry, 1)

    def test_as_dict(self):
        expected = {
            'name': self.name,
            'ip': self.ip,
            'online': self.online,
            'delay': self.delay,
            'wait': self.wait
        }
        result = self.pinger.as_dict()
        self.assertEqual(result, expected)

    def test_from_dict(self):
        name = "NewPinger"
        ip = "1.1.1.1"
        online = True
        delay = 10
        wait = 5

        payload = {
            'name': name,
            'ip': ip,
            'online': online,
            'delay': delay,
            'wait': wait
        }
        pinger = Pinger.from_dict(payload)
        self.assertEqual(pinger.as_dict(), payload)

    def test_from_dict_empty_payload(self):
        pinger = Pinger.from_dict(dict())
        self.assertEqual(pinger.name, 'NA')
        self.assertEqual(pinger.ip, '127.0.0.1')
        self.assertEqual(pinger.online, False)
        self.assertEqual(pinger.delay, 10)
        self.assertEqual(pinger.wait, 1)
