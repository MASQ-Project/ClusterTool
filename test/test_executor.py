# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from executor import Executor


class TestExecutor:

    @pytest.fixture
    def mocks(self, mocker):
        self.mock_subprocess = mocker.patch('executor.sp')
        self.mock_subprocess.PIPE = 'pipe'
        self.mock_pexpect = mocker.patch('executor.pexpect')

    def test_execute_sync(self, mocks):
        self.mock_subprocess.call.return_value = 'called'

        result = Executor().execute_sync(['one', 'two'])

        self.mock_subprocess.call.assert_called_with(['one', 'two'])
        assert result == 'called'

    def test_execute_async(self, mocks):
        self.mock_pexpect.spawn.return_value = 'spawned'

        result = Executor().execute_async(['run', 'with', 'some', 'args'])

        self.mock_pexpect.spawn.assert_called_with('run', ['with', 'some', 'args'])
        assert result == 'spawned'

    def test_execute_sync_with_output(self, mocks):
        self.mock_subprocess.Popen.return_value.communicate.return_value = 'opened'

        result = Executor().execute_sync_with_output(['run', 'with', 'args'])

        self.mock_subprocess.Popen.assert_called_with(['run', 'with', 'args'], stdout='pipe', stderr='pipe')
        assert result == 'opened'
