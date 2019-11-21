# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
import boto3
import time
from tnt_config import EC2_CONFIG
from instance_api import InstanceApi
from node_ssh_commands import NodeSshCommands
from dns_ssh_commands import DnsSshCommands
from traffic_ssh_commands import TrafficSshCommands
from traffic_handler import TrafficHandler
from node import Node
from dns import Dns


class EC2(InstanceApi):

    _machine_name = None
    node = None
    dns = None
    traffic = None

    def __init__(self, machine_name):
        self.client = boto3.client('ec2', EC2_CONFIG['region'])
        self.ip = ""
        self._machine_name = machine_name
        self.node = Node(machine_name, NodeSshCommands(self.get_external_ip))
        self.dns = Dns(machine_name, DnsSshCommands(self.get_external_ip))
        self.traffic = TrafficHandler(machine_name, TrafficSshCommands(self.get_external_ip))

    def start_instance(self):
        print('\tStarting %s EC2 instance' % self.machine_name())
        self._wait_for_a_state(['running', 'stopped'])
        response = self.client.start_instances(
            InstanceIds=[
                self._get_instance_id()
            ]
        )

    def stop_instance(self):
        print('\tStopping %s EC2 instance' % self.machine_name())
        self._wait_for_a_state(['running', 'stopped'])
        response = self.client.stop_instances(
            InstanceIds=[
                self._get_instance_id()
            ]
        )

    def restart_instance(self):
        print('\tRestarting %s EC2 instance' % self.machine_name())
        self._wait_for_a_state(['running', 'stopped'])
        response = self.client.reboot_instances(
            InstanceIds=[
                self._get_instance_id()
            ]
        )

    def get_external_ip(self):
        if self.ip == "":
            self._wait_for_external_ip()
            reservation = self._get_instance()['Reservations'][0]
            instance = reservation['Instances'][0]
            network_interface = instance['NetworkInterfaces'][0]
            private_ip_address_struct = network_interface['PrivateIpAddresses'][0]
            association = private_ip_address_struct['Association']
            public_ip = association['PublicIp']
            self.ip = public_ip
        return self.ip

    def _get_instance(self):
        response = self.client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['pending', 'running', 'shutting-down', 'stopping', 'stopped']
                },
                {
                    'Name': 'tag:Name',
                    'Values': [self.machine_name()]
                }
            ]
        )
        return response

    def _get_instance_id(self):
        reservation = self._get_instance()['Reservations'][0]
        instance = reservation['Instances'][0]
        instance_id = instance['InstanceId']
        return instance_id

    def _wait_for_external_ip(self):
        print("\t\tWaiting for external IP for %s EC2 instance..." % self.machine_name())
        while True:
            reservation = self._get_instance()['Reservations'][0]
            instance = reservation['Instances'][0]
            network_interface = instance['NetworkInterfaces'][0]
            private_ip_address_struct = network_interface['PrivateIpAddresses'][0]
            if 'Association' in private_ip_address_struct.keys() and 'PublicIp' in private_ip_address_struct['Association'].keys():
                print("\t\tdone.")
                return
            time.sleep(1)

    def _wait_for_a_state(self, state_names):
        print("\t\tWaiting for %s EC2 instance to reach a state in %s..." % (self.machine_name(), state_names))
        while True:
            description = self._get_instance()
            reservation = description['Reservations'][0]
            instance = reservation['Instances'][0]
            state = instance['State']
            actual_state_name = state['Name']
            if actual_state_name in state_names:
                print("\t\tdone.")
                return
            time.sleep(1)
