# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from dns_docker_commands import DnsDockerCommands


class TestDnsDockerCommands:

    @pytest.fixture
    def executor(self, mocker):
        self.mock_executor = mocker.patch('dns_docker_commands.Executor')
        self.mock_executor.return_value.execute_sync_with_output.return_value = 'subverted'

    def test_construction(self):
        subject = DnsDockerCommands('mario')

        assert subject.name == 'mario'

    def test_dns_utility(self, executor):
        subject = DnsDockerCommands('mario')

        result = subject.dns_utility('subvert')

        self.mock_executor.return_value.execute_sync.assert_called_with([
            'docker', 'exec', '-it', 'mario', '/node_root/node/dns_utility', 'subvert'
        ])
        self.mock_executor.return_value.execute_sync_with_output.assert_called_with([
            'docker', 'exec', '-it', 'mario', '/node_root/node/dns_utility', 'status'
        ])
        assert result == 'subverted'
