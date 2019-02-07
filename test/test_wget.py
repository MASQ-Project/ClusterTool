# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from wget import Wget, FAKE_USER_AGENT


class TestWget:

    @pytest.fixture
    def mocks(self, mocker):
        self.mock_pexpect = mocker.patch('wget.pexpect')
        self.mock_executor = mocker.Mock()

    def test_init(self, mocks):
        subject = Wget('google.com', self.mock_executor)

        assert subject.site == 'google.com'
        assert subject.p == self.mock_executor.return_value
        self.mock_executor.assert_called_with([
            'wget', '--directory-prefix=/tmp/wget/', '--page-requisites',
            '--delete-after', subject.site,
            "--user-agent='%s'" % FAKE_USER_AGENT,
            '--no-check-certificate',
        ])
        assert not subject.done
        assert subject.result == ''
        assert subject.success_pattern == \
            'HTTP request sent, awaiting response... 200 OK'

    def test_status_already_done(self, mocks):
        subject = Wget('google.com', self.mock_executor)
        subject.done = True
        subject.result = 'result'

        result = subject.status()

        assert result == 'result'

    def test_status_waiting_for_first_response(self, mocks):
        subject = Wget('google.com', self.mock_executor)
        self.mock_executor.return_value.is_alive.return_value = True
        self.mock_executor.return_value.expect.return_value = 1

        result = subject.status()

        self.mock_executor.return_value.expect.assert_called_with(
            [
                subject.success_pattern,
                self.mock_pexpect.TIMEOUT,
                self.mock_pexpect.EOF,
            ],
            timeout=1
        )

        assert result == \
            'wget google.com is still waiting for its first response'

    def test_status_still_running(self, mocks):
        subject = Wget('google.com', self.mock_executor)
        self.mock_executor.return_value.is_alive.return_value = True
        self.mock_executor.return_value.expect.return_value = 0

        result = subject.status()

        self.mock_executor.return_value.expect.assert_called_with(
            [
                subject.success_pattern,
                self.mock_pexpect.TIMEOUT,
                self.mock_pexpect.EOF,
            ],
            timeout=1
        )

        assert result == 'wget google.com traffic was successfully routed and is still running'

    def test_status_finished_successfully(self, mocks):
        subject = Wget('google.com', self.mock_executor)
        self.mock_executor.return_value.isalive.return_value = False
        self.mock_executor.return_value.exitstatus = 0
        expected_result = \
            'wget google.com (0: No problems occurred.) SUCCEEDED'

        result = subject.status()

        assert subject.done
        assert subject.result == expected_result
        assert result == expected_result

    def test_status_finished_but_failed_with_known_code(self, mocks):
        subject = Wget('google.com', self.mock_executor)
        self.mock_executor.return_value.isalive.return_value = False
        self.mock_executor.return_value.exitstatus = 1
        expected_result = \
            'wget google.com (1: Generic error code.) FAILED'

        result = subject.status()

        assert subject.done
        assert subject.result == expected_result
        assert result == expected_result

    def test_status_finished_but_failed_with_different_known_code(self, mocks):
        subject = Wget('google.com', self.mock_executor)
        self.mock_executor.return_value.isalive.return_value = False
        self.mock_executor.return_value.exitstatus = 8
        expected_result = \
            'wget google.com (8: Server issued an error response.) FAILED'

        result = subject.status()

        assert subject.done
        assert subject.result == expected_result
        assert result == expected_result

    def test_status_finished_but_failed_with_unknown_code(self, mocks):
        subject = Wget('google.com', self.mock_executor)
        self.mock_executor.return_value.isalive.return_value = False
        self.mock_executor.return_value.exitstatus = 9
        expected_result = \
            'wget google.com (9: unknown) FAILED'

        result = subject.status()

        assert subject.done
        assert subject.result == expected_result
        assert result == expected_result

    def test_cleanup(self, mocks, mocker):
        subject = Wget('google.com', self.mock_executor)
        mock_injected_executor = mocker.Mock()

        subject.cleanup(mock_injected_executor)

        self.mock_executor.return_value.terminate.assert_called_with(force=True)
        mock_injected_executor.assert_called_with(['rm -rf', '/tmp/wget/google.com'])
