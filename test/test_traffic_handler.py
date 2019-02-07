# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from traffic_handler import TrafficHandler


class TestTrafficHandler:

    @pytest.fixture
    def mocks(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print')
        self.mock_input = mocker.patch('__builtin__.raw_input')
        self.mock_curl = mocker.patch('traffic_handler.Curl')
        self.mock_wget = mocker.patch('traffic_handler.Wget')
        self.mock_traffic_commands = mocker.Mock()
        self.mock_time = mocker.patch('traffic_handler.time')

    def test_init(self):
        subject = TrafficHandler('snow', 'commands')

        assert subject.name == 'snow'
        assert subject.traffic_commands == 'commands'
        assert subject.traffic_handles == []

    def test_curl_default_site_once(self, mocks, mocker):
        subject = TrafficHandler('snow', self.mock_traffic_commands)
        self.mock_input.return_value = '1'
        self.mock_time.ctime.return_value = 'Fri Feb  1 12:29:43 2019'
        self.mock_traffic_commands.curl = 'curl command'

        subject.curl()

        self.mock_input.assert_called_with(
            'How many curls for snow? (blank line to cancel) '
        )
        assert self.mock_print.mock_calls == [
            mocker.call('\tstarting curl on snow...'),
            mocker.call(
                'Fri Feb  1 12:29:43 2019 sending curl %s #0' %
                'https://www.piday.org/million/'
            ),
            mocker.call('\tdone.'),
        ]
        assert len(subject.traffic_handles) == 1
        self.mock_curl.assert_called_with(
            'https://www.piday.org/million/', 'curl command'
        )
        self.mock_time.sleep.assert_called_with(2)

    def test_curl_other_site_twice(self, mocks, mocker):
        subject = TrafficHandler('snow', self.mock_traffic_commands)
        self.mock_input.return_value = '2'
        self.mock_time.ctime.return_value = 'Fri Feb  1 12:29:43 2019'
        self.mock_traffic_commands.curl = 'curl command'

        subject.curl('othersite.com')

        self.mock_input.assert_called_with(
            'How many curls for snow? (blank line to cancel) '
        )
        assert self.mock_print.mock_calls == [
            mocker.call('\tstarting curl on snow...'),
            mocker.call(
                'Fri Feb  1 12:29:43 2019 sending curl othersite.com #0'
            ),
            mocker.call(
                'Fri Feb  1 12:29:43 2019 sending curl othersite.com #1'
            ),
            mocker.call('\tdone.'),
        ]
        assert len(subject.traffic_handles) == 2
        assert self.mock_curl.mock_calls == [
            mocker.call('othersite.com', 'curl command'),
            mocker.call('othersite.com', 'curl command'),
        ]
        assert self.mock_time.sleep.mock_calls == [
            mocker.call(2), mocker.call(2)
        ]

    def test_curl_bootstrap(self, mocks):
        subject = TrafficHandler('bootstrap', None)

        subject.curl()

        assert self.mock_input.call_count == 0
        assert self.mock_print.call_count == 0
        assert self.mock_curl.call_count == 0
        assert not subject.traffic_handles
        assert self.mock_curl.call_count == 0
        assert self.mock_time.sleep.call_count == 0

    def test_curl_bad_input(self, mocks, mocker):
        subject = TrafficHandler('snow', self.mock_traffic_commands)
        self.mock_input.side_effect = ['NaN', '-1', '']

        subject.curl()

        assert self.mock_input.mock_calls == [
            mocker.call('How many curls for snow? (blank line to cancel) '),
            mocker.call('How many curls for snow? (blank line to cancel) '),
            mocker.call('How many curls for snow? (blank line to cancel) '),
        ]
        assert self.mock_print.mock_calls == [
            mocker.call('NaN is not a number'),
            mocker.call('-1 is not a valid number'),
        ]
        assert self.mock_curl.call_count == 0
        assert not subject.traffic_handles
        assert self.mock_curl.call_count == 0
        assert self.mock_time.sleep.call_count == 0

    def test_wget(self, mocks, mocker):
        subject = TrafficHandler('snow', self.mock_traffic_commands)
        self.mock_time.ctime.return_value = 'Fri Feb  1 12:29:43 2019'
        self.mock_traffic_commands.wget = 'wget command'

        subject.wget()

        assert self.mock_print.mock_calls == [
            mocker.call('\tstarting traffic on snow...'),
            mocker.call('Fri Feb  1 12:29:43 2019 sending wget google.com'),
            mocker.call('Fri Feb  1 12:29:43 2019 sending wget youtube.com'),
            mocker.call('Fri Feb  1 12:29:43 2019 sending wget wikipedia.org'),
            mocker.call('Fri Feb  1 12:29:43 2019 sending wget reddit.com'),
            mocker.call('Fri Feb  1 12:29:43 2019 sending wget yahoo.com'),
            mocker.call('Fri Feb  1 12:29:43 2019 sending wget amazon.com'),
            mocker.call('\tdone.'),
        ]
        assert len(subject.traffic_handles) == 6
        assert self.mock_wget.mock_calls == [
            mocker.call('google.com', 'wget command'),
            mocker.call('youtube.com', 'wget command'),
            mocker.call('wikipedia.org', 'wget command'),
            mocker.call('reddit.com', 'wget command'),
            mocker.call('yahoo.com', 'wget command'),
            mocker.call('amazon.com', 'wget command'),
        ]

    def test_wget_bootstrap(self, mocks, mocker):
        subject = TrafficHandler('bootstrap', self.mock_traffic_commands)

        subject.wget()

        assert self.mock_print.call_count == 0
        assert not subject.traffic_handles
        assert self.mock_wget.call_count == 0

    def test_stop(self, mocks, mocker):
        subject = TrafficHandler('snow', self.mock_traffic_commands)
        self.mock_traffic_commands.cleanup = 'cleanup command'
        mock_first_traffic = mocker.Mock()
        mock_second_traffic = mocker.Mock()
        subject.traffic_handles = [mock_first_traffic, mock_second_traffic]

        subject.stop()

        mock_first_traffic.cleanup.assert_called_with('cleanup command')
        mock_second_traffic.cleanup.assert_called_with('cleanup command')
        assert not subject.traffic_handles
        assert self.mock_print.mock_calls == [
            mocker.call('\tdone.')
        ]

    def test_stop_bootstrap(self, mocks):
        subject = TrafficHandler('bootstrap', self.mock_traffic_commands)

        subject.stop()

        assert self.mock_print.call_count == 0

    def test_verify(self, mocks, mocker):
        subject = TrafficHandler('snow', self.mock_traffic_commands)
        mock_first_traffic = mocker.Mock()
        mock_first_traffic.status.return_value = 'first: SUCCESS'
        mock_second_traffic = mocker.Mock()
        mock_second_traffic.status.return_value = 'second: FAILURE'
        subject.traffic_handles = [mock_first_traffic, mock_second_traffic]

        subject.verify()

        assert self.mock_print.mock_calls == [
            mocker.call('snow - first: SUCCESS'),
            mocker.call('snow - second: FAILURE'),
            mocker.call(''),
        ]

    def test_verify_no_traffic(self, mocks, mocker):
        subject = TrafficHandler('snow', self.mock_traffic_commands)

        subject.verify()

        assert self.mock_print.mock_calls == [
            mocker.call("\tyou didn't request traffic on snow")
        ]

    def test_verify_bootstrap(self, mocks):
        subject = TrafficHandler('bootstrap', self.mock_traffic_commands)

        subject.verify()

        assert self.mock_print.call_count == 0
