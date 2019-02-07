# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from traffic_docker_commands import TrafficDockerCommands


class TestTrafficDockerCommands:

    @pytest.fixture
    def executor(self, mocker):
        self.mock_executor = mocker.patch('traffic_docker_commands.Executor')

    def test_init(self, executor):
        subject = TrafficDockerCommands('beep')

        assert subject.name == 'beep'
        self.mock_executor.assert_called_with()

    def test_wget(self, executor):
        subject = TrafficDockerCommands('beep')
        self.mock_executor.return_value.execute_async.return_value = 'wgot'

        result = subject.wget(['command', 'list'])

        self.mock_executor.return_value.execute_async.assert_called_with([
            'docker', 'exec', '-it', '--workdir', '/node_root/node/', 'beep',
            'command', 'list'
        ])
        assert result == 'wgot'

    def test_curl(self, executor):
        subject = TrafficDockerCommands('beep')
        self.mock_executor.return_value.execute_async.return_value = 'curled'

        result = subject.curl(['command', 'list'])

        self.mock_executor.return_value.execute_async.assert_called_with([
            'docker', 'exec', '-it', '--workdir', '/node_root/node/', 'beep',
            'command', 'list'
        ])
        assert result == 'curled'

    def test_cleanup(self, executor):
        subject = TrafficDockerCommands('beep')
        self.mock_executor.return_value.execute_sync.return_value = 'cleaned'

        result = subject.cleanup(['command', 'list'])

        self.mock_executor.return_value.execute_sync.assert_called_with([
            'docker', 'exec', '-it', '--workdir', '/node_root/node/', 'beep',
            'command', 'list'
        ])
        assert result == 'cleaned'
