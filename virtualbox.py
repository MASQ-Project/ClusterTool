# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
import time
import pexpect
import re
import subprocess as sp
from instance_api import InstanceApi
from node_ssh_commands import NodeSshCommands
from dns_ssh_commands import DnsSshCommands
from traffic_ssh_commands import TrafficSshCommands
from traffic_handler import TrafficHandler
from node import Node
from dns import Dns


class VirtualBoxManage(InstanceApi):

    node = None
    dns = None
    traffic = None

    def __init__(self, name):
        self.ip_pattern = re.compile(r".*value: (.+), time.*")
        self.command = "VBoxManage"
        self.ip = ""
        self.name = name
        self.node = Node(name, NodeSshCommands(self.get_external_ip))
        self.dns = Dns(name, DnsSshCommands(self.get_external_ip))
        self.traffic = TrafficHandler(
            name, TrafficSshCommands(self.get_external_ip)
        )

    def start_instance(self):
        print('\tStarting %s local instance' % self.name)
        sp.call([self.command, "startvm", self.name, "--type", "headless"])

    def stop_instance(self):
        print('\tStopping %s local instance' % self.name)
        sp.call([self.command, "controlvm", self.name, "poweroff"])

    def restart_instance(self):
        print('\tRestarting %s local instance' % self.name)
        sp.call([self.command, "controlvm", self.name, "reset"])

    def get_external_ip(self):
        if self.ip == "":
            print(
                "\t\tWaiting for external IP for %s local instance..." %
                self.name
            )
            while True:
                p = pexpect.spawn(self.command, [
                    "guestproperty",
                    "enumerate",
                    self.name,
                    "get",
                    "/VirtualBox/GuestInfo/Net/0/V4/IP"
                ])
                p.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=1)
                matches = self.ip_pattern.match(p.before)

                if matches is not None:
                    print("\t\tdone.")
                    ip = matches.group(1)
                    self.ip = ip
                    break
                time.sleep(1)

        return self.ip
