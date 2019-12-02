# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function

import os
import pexpect

from executor import Executor, TerminalExecutor
from node import Node
from node_commands import *


class NodeDockerCommands(NodeCommands):

    def __init__(self, name, ip_fn):
        self.get_ip = ip_fn
        self.name = name
        self.executor = Executor()
        self.terminal_executor = TerminalExecutor(self.executor)

    def start(self, args_map, binaries_version):
        if self._exists():
            self._docker_destroy()

        return self._docker_run_node(args_map, binaries_version)

    def stop(self):
        return self.executor.execute_sync(["docker", "stop", "-t0", self.name])

    def cat_logs(self):
        command = ["docker", "exec", "-it", self.name, "cat", "/tmp/MASQNode_rCURRENT.log"]
        return self.executor.execute_async(command)

    def retrieve_logs(self, destination):
        args = [
            "docker",
            "cp",
            "%s:%s" % (self.name, MASQ_NODE_LOG),
            destination,
        ]
        return self.executor.execute_sync(args)

    def update(self, binary, irrelevant):
        print("Binaries are volume-mapped for Docker-based Nodes; no update is required.")
        return 0

    def tail(self):
        command = "\"{0}({1})\" docker exec -it {0} tail -f -n 250 /tmp/MASQNode_rCURRENT.log".format(self.name,
                                                                                                   self.get_ip(),
                                                                                                   self.name)
        return self.terminal_executor.execute_in_new_terminal(command)

    def shell(self):
        command = "\"{0}({1})\" docker exec -it {0} bash".format(self.name, self.get_ip())
        return self.terminal_executor.execute_in_new_terminal(command)

    def delete_logs(self):
        pass

    def _docker_run_node(self, args_map, binaries_version):
        volume = "%s/binaries/:/node_root/node" % os.getcwd()
        if binaries_version is not None:
            volume = "%s/binaries/%s/:/node_root/node" % (os.getcwd(), binaries_version)
        command_prefix = [
            "docker",
            "run",
            "--detach",
            "--ip", self.get_ip(),
            "--dns", "127.0.0.1",
            "--name", self.name,
            "--hostname", self.name,
            "--net", "test_net",
            "--volume", volume,
            "test_net_tools",
            "/node_root/node/MASQNode"
        ]
        sorted_keys = sorted(args_map.keys())
        command = reduce(lambda sofar, key: sofar + ["--%s" % key, args_map[key]], sorted_keys, command_prefix)
        return self.executor.execute_sync(command)

    def _docker_destroy(self):
        command = [
            "docker", "rm", "-f", self.name
        ]
        return self.executor.execute_sync(command)

    def _exists(self):
        command = [
            "docker", "ps", "--all", "-q", "-f name=%s" % self.name,
        ]
        p = self.executor.execute_async(command)
        idx = p.expect(['[0-9a-fA-F]+', pexpect.EOF], timeout=None)
        return True if idx == 0 else False
