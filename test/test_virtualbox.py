# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import re
from virtualbox import VirtualBoxManage


class TestVirtualBoxManage:

    @pytest.fixture
    def mocks(self, mocker):
        self.mock_node = mocker.patch('virtualbox.Node')
        self.mock_dns = mocker.patch('virtualbox.Dns')
        self.mock_traffic = mocker.patch('virtualbox.TrafficHandler')
        self.mock_node_ssh_commands = \
            mocker.patch('virtualbox.NodeSshCommands')
        self.mock_dns_ssh_commands = mocker.patch('virtualbox.DnsSshCommands')
        self.mock_traffic_ssh_commands = \
            mocker.patch('virtualbox.TrafficSshCommands')
        self.mock_print = mocker.patch('__builtin__.print')
        self.mock_sp = mocker.patch('virtualbox.sp')
        self.mock_pexpect = mocker.patch('virtualbox.pexpect')
        self.mock_time = mocker.patch('virtualbox.time')

    def test_init(self, mocks):
        subject = VirtualBoxManage('vbox')

        assert subject.ip_pattern == re.compile(r'.*value: (.+), time.*')
        assert subject.command == 'VBoxManage'
        assert subject.ip == ''
        assert subject.machine_name() == 'vbox'
        self.mock_node.assert_called_with(
            'vbox',
            self.mock_node_ssh_commands.return_value
        )
        self.mock_node_ssh_commands.assert_called_with(subject.get_external_ip)
        self.mock_dns.assert_called_with(
            'vbox',
            self.mock_dns_ssh_commands.return_value
        )
        self.mock_dns_ssh_commands.assert_called_with(subject.get_external_ip)
        self.mock_traffic.assert_called_with(
            'vbox',
            self.mock_traffic_ssh_commands.return_value
        )
        self.mock_traffic_ssh_commands.assert_called_with(
            subject.get_external_ip
        )

    def test_start_instance(self, mocks):
        subject = VirtualBoxManage('vbox')

        subject.start_instance()

        self.mock_print.assert_called_with('\tStarting vbox local instance')
        self.mock_sp.call.assert_called_with([
            subject.command,
            'startvm',
            subject.machine_name(),
            '--type',
            'headless',
        ])

    def test_stop_instance(self, mocks):
        subject = VirtualBoxManage('vbox')

        subject.stop_instance()

        self.mock_print.assert_called_with('\tStopping vbox local instance')
        self.mock_sp.call.assert_called_with([
            subject.command,
            'controlvm',
            subject.machine_name(),
            'poweroff',
        ])

    def test_restart_instance(self, mocks):
        subject = VirtualBoxManage('vbox')

        subject.restart_instance()

        self.mock_print.assert_called_with('\tRestarting vbox local instance')
        self.mock_sp.call.assert_called_with([
            subject.command,
            'controlvm',
            subject.machine_name(),
            'reset',
        ])

    def test_get_external_ip(self, mocks, mocker):
        subject = VirtualBoxManage('vbox')
        first_spawn = mocker.Mock()
        second_spawn = mocker.Mock()
        self.mock_pexpect.spawn.side_effect = [
            first_spawn,
            second_spawn
        ]
        first_spawn.before = ''
        second_spawn.before = 'stuff, value: 1.2.3.4, time other stuff'

        result = subject.get_external_ip()

        assert self.mock_print.mock_calls == [
            mocker.call(
                '\t\tWaiting for external IP for vbox local instance...'
            ),
            mocker.call('\t\tdone.'),
        ]
        self.mock_pexpect.spawn.assert_called_with(subject.command, [
            'guestproperty',
            'enumerate',
            subject.machine_name(),
            'get',
            '/VirtualBox/GuestInfo/Net/0/V4/IP'
        ])
        first_spawn.expect.assert_called_with(
            [self.mock_pexpect.TIMEOUT, self.mock_pexpect.EOF],
            timeout=1
        )
        second_spawn.expect.assert_called_with(
            [self.mock_pexpect.TIMEOUT, self.mock_pexpect.EOF],
            timeout=1
        )

        self.mock_time.sleep.assert_called_with(1)

        assert subject.ip == '1.2.3.4'
        assert result == '1.2.3.4'

    def test_get_saved_ip(self, mocks, mocker):
        subject = VirtualBoxManage('vbox')
        subject.ip = '2.3.4.5'

        result = subject.get_external_ip()

        assert self.mock_print.call_count == 0
        assert self.mock_pexpect.spawn.call_count == 0
        assert self.mock_pexpect.spawn.return_value.expect.call_count == 0

        assert subject.ip == '2.3.4.5'
        assert result == '2.3.4.5'
