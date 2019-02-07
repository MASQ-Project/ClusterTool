# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
import googleapiclient.discovery
import time
from instance_api import InstanceApi
from tnt_config import COMPUTE_CONFIG
from node_ssh_commands import NodeSshCommands
from dns_ssh_commands import DnsSshCommands
from traffic_ssh_commands import TrafficSshCommands
from traffic_handler import TrafficHandler
from node import Node
from dns import Dns


class Compute(InstanceApi):

    node = None
    dns = None
    traffic = None

    def __init__(self, name, project=COMPUTE_CONFIG['project'], zone=COMPUTE_CONFIG['zone']):
        self.compute = googleapiclient.discovery.build('compute', 'v1')
        self.project = project
        self.zone = zone
        self.ip = ""
        self.name = name
        self.node = Node(name, NodeSshCommands(self.get_external_ip))
        self.dns = Dns(name, DnsSshCommands(self.get_external_ip))
        self.traffic = TrafficHandler(name, TrafficSshCommands(self.get_external_ip))

    def start_instance(self):
        print('\tStarting %s Compute instance' % self.name)
        return self.compute.instances().start(project=self.project, zone=self.zone, instance=self.name).execute()

    def stop_instance(self):
        print('\tStopping %s Compute instance' % self.name)
        return self.compute.instances().stop(project=self.project, zone=self.zone, instance=self.name).execute()

    def restart_instance(self):
        print('\tRestarting %s Compute instance' % self.name)
        return self.compute.instances().reset(project=self.project, zone=self.zone, instance=self.name).execute()

    def get_external_ip(self):
        if self.ip == "":
            self._wait_for_external_ip()
            interfaces = self._get_instance()['networkInterfaces']
            configs = interfaces[0]['accessConfigs']
            ip = configs[0]['natIP']
            self.ip = ip

        return self.ip

    def _list_instances(self):
        return self.compute.instances().list(project=self.project, zone=self.zone).execute()

    def _get_instance(self):
        for instance in self._list_instances()['items']:
            if instance['name'] == self.name:
                return instance

    def _wait_for_external_ip(self):
        print("\t\tWaiting for external IP for %s Compute instance..." % self.name)
        while True:
            instance = self._get_instance()
            interfaces = instance['networkInterfaces']
            configs = interfaces[0]['accessConfigs']
            if 'natIP' in configs[0].keys():
                print("\t\tdone.")
                return
            time.sleep(1)
