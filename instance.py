# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
BINARIES = [
    "SubstratumNode",
    "dns_utility",
]


class Instance:
    def __init__(self, name, instance_api):
        self.name = name
        self.instance_api = instance_api
        self.dns = self.instance_api.dns
        self.traffic = self.instance_api.traffic
        self.node = self.instance_api.node

    def start(self):
        self.instance_api.start_instance()
        return self

    def kill(self):
        return self.instance_api.stop_instance()

    def restart(self):
        return self.instance_api.restart_instance()

    def get_ip(self):
        return self.instance_api.get_external_ip()

    def shell(self):
        self.node.shell()

    def update(self):
        self.node.update()

    def start_node(self, bootstrap_info=""):
        return self.node.start(self.get_ip(), bootstrap_info)

    def stop_node(self):
        self.dns.revert()
        self.traffic.stop()
        self.node.shutdown()

    def retrieve_logs(self, to_dir="/tmp"):
        self.node.retrieve_logs(to_dir)

    def tail(self):
        self.node.tail()

    def inspect(self):
        self.node.display_neighborhood()

    def inbound(self):
        self.node.gossip_received()

    def outbound(self):
        self.node.gossip_produced()

    def subvert(self):
        self.dns.subvert()

    def revert(self):
        self.traffic.stop()
        self.dns.revert()

    def verify(self):
        self.traffic.verify()

    def curl(self):
        self.dns.subvert()
        self.traffic.curl()

    def wget(self):
        self.dns.subvert()
        self.traffic.wget()

