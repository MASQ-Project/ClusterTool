# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from dns_commands import DnsCommands
from executor import Executor

DNS_BINARY = "/node_root/node/dns_utility"


class DnsDockerCommands(DnsCommands):
    def __init__(self, name):
        self.name = name
        self.executor = Executor()
        
    def dns_utility(self, command):
        dns_command = [
            "docker", "exec", "-it", self.name, DNS_BINARY,
        ]
        self.executor.execute_sync(dns_command + [command])
        return self.executor.execute_sync_with_output(dns_command + ["status"])
