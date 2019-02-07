# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from traffic_ssh_commands import TrafficSshCommands


class TestTrafficSshCommands:

    @pytest.fixture
    def mocks(self, mocker):
        self.mock_executor = mocker.patch('traffic_ssh_commands.Executor')
        self.mock_tnt_config = mocker.patch('traffic_ssh_commands.tnt_config')
        self.mock_tnt_config.INSTANCE_USER = 'mockeduser'

    def test_init(self, mocks):
        subject = TrafficSshCommands(lambda: '1.2.3.4')

        assert subject.get_ip() == '1.2.3.4'

    def test_wget(self, mocks):
        subject = TrafficSshCommands(lambda: '1.2.3.4')
        self.mock_executor.return_value.execute_async.return_value = 'wgot'

        result = subject.wget(['one', 'two'])

        self.mock_executor.return_value.execute_async.assert_called_with([
            'ssh', '-oStrictHostKeyChecking=no',
            'mockeduser@1.2.3.4',
            'one', 'two'
        ])
        assert result == 'wgot'

    def test_curl(self, mocks):
        subject = TrafficSshCommands(lambda: '1.2.3.4')
        self.mock_executor.return_value.execute_async.return_value = 'curled'

        result = subject.curl(['one', 'two'])

        self.mock_executor.return_value.execute_async.assert_called_with([
            'ssh', '-oStrictHostKeyChecking=no',
            'mockeduser@1.2.3.4',
            'one', 'two'
        ])
        assert result == 'curled'

    def test_cleanup(self, mocks):
        subject = TrafficSshCommands(lambda: '1.2.3.4')
        self.mock_executor.return_value.execute_async.return_value = 'cleaned'

        result = subject.cleanup(['one', 'two'])

        self.mock_executor.return_value.execute_async.assert_called_with([
            'ssh', '-oStrictHostKeyChecking=no',
            'mockeduser@1.2.3.4',
            'one', 'two'
        ])
        assert result == 'cleaned'
