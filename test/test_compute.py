# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from compute import Compute


class TestCompute:

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print')

    @pytest.fixture
    def time(self, mocker):
        self.mock_time = mocker.patch('compute.time')

    @pytest.fixture
    def compute(self, mocker, printing):
        self.mock_compute = mocker.patch('compute.googleapiclient.discovery.build', autospec=True)
        self.mock_compute.return_value\
            .instances.return_value\
            .list.return_value\
            .execute.side_effect = [
                {
                    'items': [{
                        'name': 'Google', 'networkInterfaces': [{
                            'accessConfigs': [{'noIpYet': ''}]
                        }]
                    }]
                },
                {
                    'items': [{
                        'name': 'Google', 'networkInterfaces': [{
                            'accessConfigs': [{'natIP': '1.2.3.4'}]
                        }]
                    }]
                },
                {
                    'items': [{
                        'name': 'Google', 'networkInterfaces': [{
                            'accessConfigs': [{'natIP': '1.2.3.4'}]
                        }]
                    }]
                }
            ]
        self.mock_start = self.mock_compute.return_value.instances.return_value.start
        self.mock_start.return_value.execute.return_value = "started"

        self.mock_stop = self.mock_compute.return_value.instances.return_value.stop
        self.mock_stop.return_value.execute.return_value = "stopped"

        self.mock_reset = self.mock_compute.return_value.instances.return_value.reset
        self.mock_reset.return_value.execute.return_value = "reset"

    @pytest.fixture
    def node_ssh_commands(self, mocker):
        self.mock_node_ssh_commands = mocker.patch('compute.NodeSshCommands')

    @pytest.fixture
    def dns_ssh_commands(self, mocker):
        self.mock_dns_ssh_commands = mocker.patch('compute.DnsSshCommands')

    @pytest.fixture
    def traffic_ssh_commands(self, mocker):
        self.mock_traffic_ssh_commands = mocker.patch('compute.TrafficSshCommands')

    def test_construction(self, compute):
        subject = Compute('Google', 'project', 'usa')

        self.mock_compute.assert_called_with('compute', 'v1')
        assert subject.project == 'project'
        assert subject.zone == 'usa'
        assert subject.ip == ''
        assert subject.machine_name() == 'Google'
        assert subject.node.machine_name() == 'Google'
        assert subject.dns.machine_name() == 'Google'
        assert subject.traffic.machine_name() == 'Google'

    def test_node_property(self, compute, node_ssh_commands):
        subject = Compute('Google', 'project', 'usa')

        subject.node.shell()

        self.mock_node_ssh_commands.assert_called_with(subject.get_external_ip)
        self.mock_node_ssh_commands.return_value.shell.assert_called_with()

    def test_dns_property(self, compute, dns_ssh_commands):
        subject = Compute('Google', 'project', 'usa')

        self.mock_dns_ssh_commands.assert_called_with(subject.get_external_ip)

    def test_traffic_property(self, compute, traffic_ssh_commands):
        subject = Compute('Google', 'project', 'usa')

        self.mock_traffic_ssh_commands.assert_called_with(subject.get_external_ip)

    def test_start_instance(self, printing, compute):
        subject = Compute('Startable', 'start project', 'startosphere')

        result = subject.start_instance()

        self.mock_print.assert_called_with('\tStarting Startable Compute instance')
        self.mock_start.assert_called_with(project='start project', zone='startosphere', instance='Startable')
        assert result == 'started'

    def test_stop_instance(self, printing, compute):
        subject = Compute('Stoppable', 'stop project', 'stoposphere')

        result = subject.stop_instance()

        self.mock_print.assert_called_with('\tStopping Stoppable Compute instance')
        self.mock_stop.assert_called_with(project='stop project', zone='stoposphere', instance='Stoppable')
        assert result == 'stopped'

    def test_restart_instance(self, printing, compute):
        subject = Compute('Resettable', 'reset project', 'resetosphere')

        result = subject.restart_instance()

        self.mock_print.assert_called_with('\tRestarting Resettable Compute instance')
        self.mock_reset.assert_called_with(project='reset project', zone='resetosphere', instance='Resettable')
        assert result == 'reset'

    def test_get_external_ip(self, mocker, printing, compute, time):
        subject = Compute('Google', 'project', 'usa')

        result = subject.get_external_ip()

        self.mock_compute.return_value.instances.return_value.list.assert_called_with(project='project', zone='usa')
        self.mock_print.assert_has_calls([
            mocker.call('\t\tWaiting for external IP for Google Compute instance...'),
            mocker.call('\t\tdone.')
        ])
        self.mock_time.sleep.assert_called_with(1)
        assert result == '1.2.3.4'
