# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from ec2 import EC2, EC2_CONFIG


class TestEC2:

    @pytest.fixture
    def boto3(self, mocker):
        self.mock_boto3 = mocker.patch('ec2.boto3')
        self.mock_boto3.client.return_value.describe_instances.side_effect = [
            {
                'Reservations': [
                    {'Instances': [
                        {
                            'InstanceId': 'foo',
                            'NetworkInterfaces': [
                                {'PrivateIpAddresses': [
                                    {'nothingyet': {'PublicIp': ''}}
                                ]}
                            ],
                            'State': {'Name': 'pending'}
                        }
                    ]}
                ]
            },
            {
                'Reservations': [
                    {'Instances': [
                        {
                            'InstanceId': 'foo',
                            'NetworkInterfaces': [
                                {'PrivateIpAddresses': [
                                    {'Association': {'PublicIp': '1.2.3.4'}}
                                ]}
                            ],
                            'State': {'Name': 'running'}
                        }
                    ]}
                ]
            },
            {
                'Reservations': [
                    {'Instances': [
                        {
                            'InstanceId': 'foo',
                            'NetworkInterfaces': [
                                {'PrivateIpAddresses': [
                                    {'Association': {'PublicIp': '1.2.3.4'}}
                                ]}
                            ],
                            'State': {'Name': 'running'}
                        }
                    ]}
                ]
            }
        ]

    @pytest.fixture
    def time(self, mocker):
        self.mock_time = mocker.patch('ec2.time')

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print')

    @pytest.fixture
    def node_ssh_commands(self, mocker):
        self.mock_node_ssh_commands = mocker.patch('ec2.NodeSshCommands')

    @pytest.fixture
    def dns_ssh_commands(self, mocker):
        self.mock_dns_ssh_commands = mocker.patch('ec2.DnsSshCommands')

    @pytest.fixture
    def traffic_ssh_commands(self, mocker):
        self.mock_traffic_ssh_commands = mocker.patch('ec2.TrafficSshCommands')

    def test_construction(self, boto3):
        subject = EC2('Thor')

        self.mock_boto3.client.assert_called_with('ec2', EC2_CONFIG['region'])
        assert subject.name == 'Thor'
        assert subject.ip == ''

    def test_node_property(self, boto3, node_ssh_commands):
        subject = EC2('Amazon')

        subject.node.shell()

        self.mock_node_ssh_commands.assert_called_with(subject.get_external_ip)
        self.mock_node_ssh_commands.return_value.shell.assert_called_with()

    def test_dns_property(self, boto3, dns_ssh_commands):
        subject = EC2('Amazon')

        self.mock_dns_ssh_commands.assert_called_with(subject.get_external_ip)

    def test_traffic_property(self, boto3, traffic_ssh_commands):
        subject = EC2('Amazon')

        self.mock_traffic_ssh_commands.assert_called_with(subject.get_external_ip)

    def test_start_instance(self, mocker, printing, time, boto3):
        subject = EC2('Thor')

        subject.start_instance()

        assert self.mock_print.mock_calls == [
            mocker.call('\tStarting Thor EC2 instance'),
            mocker.call("\t\tWaiting for Thor EC2 instance to reach a state in ['running', 'stopped']..."),
            mocker.call('\t\tdone.')
        ]
        self.mock_time.sleep.assert_called_with(1)
        self.mock_boto3.client.return_value.start_instances.assert_called_with(InstanceIds=['foo'])

    def test_stop_instance(self, mocker, printing, time, boto3):
        subject = EC2('Thor')

        subject.stop_instance()

        assert self.mock_print.mock_calls == [
            mocker.call('\tStopping Thor EC2 instance'),
            mocker.call("\t\tWaiting for Thor EC2 instance to reach a state in ['running', 'stopped']..."),
            mocker.call('\t\tdone.')
        ]
        self.mock_time.sleep.assert_called_with(1)
        self.mock_boto3.client.return_value.stop_instances.assert_called_with(InstanceIds=['foo'])

    def test_restart_instance(self, mocker, printing, time, boto3):
        subject = EC2('Thor')

        subject.restart_instance()

        assert self.mock_print.mock_calls == [
            mocker.call('\tRestarting Thor EC2 instance'),
            mocker.call("\t\tWaiting for Thor EC2 instance to reach a state in ['running', 'stopped']..."),
            mocker.call('\t\tdone.')
        ]
        self.mock_time.sleep.assert_called_with(1)
        self.mock_boto3.client.return_value.reboot_instances.assert_called_with(InstanceIds=['foo'])

    def test_get_external_ip(self, boto3, printing, time, mocker):
        subject = EC2('Thor')

        result = subject.get_external_ip()

        assert self.mock_print.mock_calls == [
            mocker.call('\t\tWaiting for external IP for Thor EC2 instance...'),
            mocker.call('\t\tdone.')
        ]
        self.mock_time.sleep.assert_called_with(1)
        assert result == '1.2.3.4'