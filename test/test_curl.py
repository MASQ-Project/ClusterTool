# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from curl import Curl


class TestCurl:

    @pytest.fixture
    def executor(self, mocker):
        self.mock_executor = mocker.Mock()

    def test_construction_fields(self, mocker):
        subject = Curl('www.google.com', mocker.stub())

        assert subject.site == 'www.google.com'
        assert subject.done is False
        assert subject.result == ''

    def test_construction_process(self, executor):
        subject = Curl('www.google.com', self.mock_executor)

        subject.p()

        self.mock_executor.assert_called_with(['curl', '-s', 'www.google.com'])

    def test_status_when_already_done_and_queried(self, executor):
        subject = Curl('www.yahoo.com', self.mock_executor)
        subject.result = 'result'
        subject.done = True

        result = subject.status()

        assert result == 'result'

    def test_status_while_still_executing(self, executor):
        self.mock_executor.return_value.isalive.return_value = True
        subject = Curl('www.yahoo.com', self.mock_executor)

        result = subject.status()

        assert result == 'curl www.yahoo.com is still waiting for a response'

    def test_status_with_successful_exit_code(self, executor):
        self.mock_executor.return_value.isalive.return_value = False
        self.mock_executor.return_value.exitstatus = 0
        subject = Curl('www.yahoo.com', self.mock_executor)

        result = subject.status()

        assert subject.done is True
        assert subject.result == 'curl www.yahoo.com (0: Success) SUCCEEDED'
        assert result == 'curl www.yahoo.com (0: Success) SUCCEEDED'

    def test_status_with_1_exit_code(self, executor):
        self.mock_executor.return_value.isalive.return_value = False
        self.mock_executor.return_value.exitstatus = 1
        subject = Curl('www.yahoo.com', self.mock_executor)

        result = subject.status()

        assert subject.done is True
        assert subject.result == 'curl www.yahoo.com (1: Unsupported protocol. This build of curl has no support for this protocol.) FAILED'
        assert result == 'curl www.yahoo.com (1: Unsupported protocol. This build of curl has no support for this protocol.) FAILED'

    def test_status_with_77_exit_code(self, executor):
        self.mock_executor.return_value.isalive.return_value = False
        self.mock_executor.return_value.exitstatus = 77
        subject = Curl('www.yahoo.com', self.mock_executor)

        result = subject.status()

        assert subject.done is True
        assert subject.result == 'curl www.yahoo.com (77: SSL public key does not matched pinned public key) FAILED'
        assert result == 'curl www.yahoo.com (77: SSL public key does not matched pinned public key) FAILED'

    def test_status_with_unknown_exit_code(self, executor):
        self.mock_executor.return_value.isalive.return_value = False
        self.mock_executor.return_value.exitstatus = 78
        subject = Curl('www.yahoo.com', self.mock_executor)

        result = subject.status()

        assert subject.done is True
        assert subject.result == 'curl www.yahoo.com (78: unknown) FAILED'
        assert result == 'curl www.yahoo.com (78: unknown) FAILED'

    def test_cleanup(self, mocker, executor):
        subject = Curl('www.nyan.cat', self.mock_executor)

        subject.cleanup(mocker.stub())

        self.mock_executor.return_value.terminate.assert_called_with(force=True)
