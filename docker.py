# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from instance_api import InstanceApi
from tnt_config import INSTANCES
from executor import Executor
from node import Node
from dns import Dns
from node_docker_commands import NodeDockerCommands
from dns_docker_commands import DnsDockerCommands
from traffic_docker_commands import TrafficDockerCommands
from traffic_handler import TrafficHandler
import pexpect


class Docker(InstanceApi):

    node = None
    dns = None
    traffic = None

    def __init__(self, name, instance_index):
        self.name = name
        self.instance_index = instance_index
        self.executor = Executor()
        self.node = Node(name, NodeDockerCommands(name, self.get_external_ip))
        self.dns = Dns(name, DnsDockerCommands(name))
        self.traffic = TrafficHandler(name, TrafficDockerCommands(name))

    def start_instance(self):
        if not self._network_exists():
            self._create_network()

    def stop_instance(self):
        self._docker_remove_container()
        self._docker_remove_network()
        self.node.descriptor = ""
    
    def restart_instance(self):
        self.stop_instance()
        self.start_instance()

    def get_external_ip(self):
        return "172.20.0.%s" % self.instance_index

    def _network_exists(self):
        command = [
            "docker", "network", "list", "--filter", "name=test_net"
        ]
        p = self.executor.execute_async(command)
        idx = p.expect(["test_net", pexpect.EOF], timeout=None)
        return True if idx == 0 else False

    def _create_network(self):
        command = [
            "docker", "network", "create", "--subnet", "172.20.0.0/16", "test_net"
        ]
        print("\tCreating the docker network test_net")
        (stdoutdata, stderrdata) = self.executor.execute_sync_with_output(command)
        print(stderrdata)

    def _docker_remove_container(self):
        command = [
            "docker", "container", "rm", "--force", self.name
        ]
        print("\tRemoving docker container %s" % self.name)
        (stdoutdata, stderrdata) = self.executor.execute_sync_with_output(command)
        print(stderrdata)
    
    def _docker_remove_network(self):
        if self._is_last_container() and self._network_exists():
            command = [
                "docker", "network", "remove", "test_net"
            ]
            print("\tRemoving docker network test_net")
            return self.executor.execute_sync_with_output(command)
        
    def _is_last_container(self):
        return True if len(INSTANCES) == 1 else False