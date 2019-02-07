# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from dns import Dns


class TestDns:

    @pytest.fixture
    def commands(self, mocker):
        self.mock_commands = mocker.Mock()

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print')

    def test_construction(self):
        subject = Dns('nodename', 'commands')

        assert subject.name == 'nodename'
        assert subject.dns_commands == 'commands'
        assert subject.dns_status == ''

    def test_subvert_bootstrap(self, commands, printing):
        subject = Dns('bootstrap', self.mock_commands)

        subject.subvert()

        assert self.mock_print.call_count == 0

    def test_subvert_standard(self, mocker, commands, printing):
        subject = Dns('standard', self.mock_commands)
        self.mock_commands.dns_utility.return_value = ("subverted", "")

        subject.subvert()

        assert self.mock_print.mock_calls == [
            mocker.call('\tsubverting DNS on standard...'),
            mocker.call('\tdone.')
        ]
        self.mock_commands.dns_utility.assert_called_with('subvert')
        assert subject.dns_status == 'subverted'
        self.mock_print.reset()

        subject.subvert()

        self.mock_print.assert_called_with('standard already subverted')

    def test_revert_bootstrap(self, commands, printing):
        subject = Dns('bootstrap', self.mock_commands)

        subject.revert()

        assert self.mock_print.call_count == 0

    def test_revert_standard(self, mocker, commands, printing):
        subject = Dns('standard', self.mock_commands)
        self.mock_commands.dns_utility.return_value = ("reverted", "")

        subject.revert()

        assert self.mock_print.mock_calls == [
            mocker.call('\treverting DNS on standard...'),
            mocker.call('\tdone.')
        ]
        self.mock_commands.dns_utility.assert_called_with('revert')
        assert subject.dns_status == 'reverted'
        self.mock_print.reset()

        subject.revert()

        self.mock_print.assert_called_with('standard already reverted')
