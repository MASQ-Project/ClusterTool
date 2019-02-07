# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from dns_ssh_commands import DnsSshCommands


class TestDnsSshCommands:

    @pytest.fixture
    def mocks(self, mocker):
        self.mock_executor = mocker.patch('dns_ssh_commands.Executor')
        self.mock_executor.return_value.execute_sync_with_output.return_value = 'reverted'
        self.mock_ip_fn = mocker.Mock()
        self.mock_ip_fn.return_value = '1.2.3.4'
        self.mock_tnt_config = mocker.patch('dns_ssh_commands.tnt_config')
        self.mock_tnt_config.INSTANCE_USER = 'mockeduser'

    def test_construction(self, mocks):
        subject = DnsSshCommands(self.mock_ip_fn)

        assert subject.get_ip() == '1.2.3.4'

    def test_dns_utility(self, mocks):
        subject = DnsSshCommands(self.mock_ip_fn)

        result = subject.dns_utility('revert')

        self.mock_executor.return_value.execute_sync_with_output.assert_called_with([
            'ssh', '-oStrictHostKeyChecking=no', 'mockeduser@1.2.3.4',
            'sudo ./dns_utility revert; ./dns_utility status'
        ])
        assert result == 'reverted'
