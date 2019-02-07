# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from docker import Docker
import pexpect


class TestDocker:

    @pytest.fixture
    def executor(self, mocker):
        self.mock_executor = mocker.patch('docker.Executor')

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print')

    @pytest.fixture
    def last_instance(self, mocker):
        mocker.patch.dict('docker.INSTANCES', first='Anakin')

    @pytest.fixture
    def node_docker_commands(self, mocker):
        self.mock_node_docker_commands = mocker.patch('docker.NodeDockerCommands')

    @pytest.fixture
    def dns_docker_commands(self, mocker):
        self.mock_dns_docker_commands = mocker.patch('docker.DnsDockerCommands')

    @pytest.fixture
    def traffic_docker_commands(self, mocker):
        self.mock_traffic_docker_commands = mocker.patch('docker.TrafficDockerCommands')

    def test_construction_properties(self):
        subject = Docker('mario', 27)

        assert subject.name == 'mario'
        assert subject.instance_index == 27

    def test_construction_executor(self, executor):
        self.mock_executor.return_value = 'executor instance'

        subject = Docker('mario', 27)

        self.mock_executor.assert_called_with()
        assert subject.executor == 'executor instance'

    def test_node_property(self, node_docker_commands):
        subject = Docker('mario', 27)

        subject.node.shell()

        self.mock_node_docker_commands.assert_called_with(subject.name, subject.get_external_ip)
        self.mock_node_docker_commands.return_value.shell.assert_called_with()

    def test_dns_property(self, dns_docker_commands):
        subject = Docker('mario', 27)

        self.mock_dns_docker_commands.assert_called_with(subject.name)

    def test_traffic_property(self, traffic_docker_commands):
        subject = Docker('mario', 27)

        self.mock_traffic_docker_commands.assert_called_with(subject.name)

    def test_start_instance_when_network_does_not_exist(self, mocker, executor, printing):
        self.mock_executor.return_value.execute_async.return_value.expect.return_value = 1  # didn't find test_net
        self.mock_executor.return_value.execute_sync_with_output.return_value = ('', 'created test_net')
        subject = Docker('mario', 27)

        subject.start_instance()

        self.mock_executor.return_value.execute_async.assert_called_with([
            'docker', 'network', 'list', '--filter', 'name=test_net'
        ])
        self.mock_executor.return_value.execute_async.return_value.expect.assert_called_with([
            'test_net', pexpect.EOF
        ], timeout=None)

        assert self.mock_print.mock_calls == [
            mocker.call('\tCreating the docker network test_net'),
            mocker.call('created test_net')
        ]
        self.mock_executor.return_value.execute_sync_with_output.assert_called_with([
            'docker', 'network', 'create', '--subnet', '172.20.0.0/16', 'test_net'
        ])

    def test_start_instance_when_network_exists(self, executor, printing):
        self.mock_executor.return_value.execute_async.return_value.expect.return_value = 0  # found test_net
        subject = Docker('mario', 27)

        subject.start_instance()

        self.mock_executor.return_value.execute_async.assert_called_with([
            'docker', 'network', 'list', '--filter', 'name=test_net'
        ])
        self.mock_executor.return_value.execute_async.return_value.expect.assert_called_with([
            'test_net', pexpect.EOF
        ], timeout=None)

        assert self.mock_print.call_count == 0
        assert self.mock_executor.return_value.execute_sync_with_output.call_count == 0

    def test_stop_instance(self, mocker, executor, printing):
        self.mock_executor.return_value.execute_sync_with_output.return_value = ('', 'removed container')
        subject = Docker('mario', 27)

        subject.stop_instance()

        assert self.mock_print.mock_calls == [
            mocker.call('\tRemoving docker container mario'),
            mocker.call('removed container')
        ]
        self.mock_executor.return_value.execute_sync_with_output.assert_called_with([
            'docker', 'container', 'rm', '--force', 'mario'
        ])
        assert subject.node.descriptor == ''

    def test_stop_last_instance(self, mocker, executor, printing, last_instance):
        self.mock_executor.return_value.execute_async.return_value.expect.return_value = 0  # found test_net
        self.mock_executor.return_value.execute_sync_with_output.return_value = ('', 'removed container')
        subject = Docker('mario', 27)

        subject.stop_instance()

        assert self.mock_print.mock_calls == [
            mocker.call('\tRemoving docker container mario'),
            mocker.call('removed container'),
            mocker.call('\tRemoving docker network test_net')
        ]
        assert self.mock_executor.return_value.execute_sync_with_output.mock_calls == [
            mocker.call(['docker', 'container', 'rm', '--force', 'mario']),
            mocker.call(['docker', 'network', 'remove', 'test_net'])
        ]

        self.mock_executor.return_value.execute_async.assert_called_with([
            'docker', 'network', 'list', '--filter', 'name=test_net'
        ])
        self.mock_executor.return_value.execute_async.return_value.expect.assert_called_with([
            'test_net', pexpect.EOF
        ], timeout=None)

    def test_restart_instance(self, mocker, executor, printing):
        self.mock_executor.return_value.execute_async.return_value.expect.return_value = 1  # didn't find test_net
        self.mock_executor.return_value.execute_sync_with_output.side_effect = [
            ('', 'removed container'),
            ('', 'created network')
        ]
        subject = Docker('mario', 27)

        subject.restart_instance()

        assert self.mock_print.mock_calls == [
            mocker.call('\tRemoving docker container mario'),
            mocker.call('removed container'),
            mocker.call('\tCreating the docker network test_net'),
            mocker.call('created network')
        ]
        assert self.mock_executor.return_value.execute_sync_with_output.mock_calls == [
            mocker.call(['docker', 'container', 'rm', '--force', 'mario']),
            mocker.call(['docker', 'network', 'create', '--subnet', '172.20.0.0/16', 'test_net']),
        ]

        self.mock_executor.return_value.execute_async.assert_called_with([
            'docker', 'network', 'list', '--filter', 'name=test_net'
        ])
        self.mock_executor.return_value.execute_async.return_value.expect.assert_called_with([
            'test_net', pexpect.EOF
        ], timeout=None)

    def test_get_external_ip(self):
        subject = Docker('mario', 27)

        result = subject.get_external_ip()

        assert result == '172.20.0.27'
