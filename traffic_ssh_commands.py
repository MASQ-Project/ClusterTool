# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from traffic_commands import TrafficCommands
from ssh_wrapper import wrap_with_ssh
import tnt_config
from executor import Executor


class TrafficSshCommands(TrafficCommands):
    def __init__(self, ip_fn):
        self.get_ip = ip_fn
        self.executor = Executor()

    def wget(self, command_list):
        return self._ssh_the_commands(command_list)

    def curl(self, command_list):
        return self._ssh_the_commands(command_list)

    def cleanup(self, command_list):
        return self._ssh_the_commands(command_list)

    def _ssh_the_commands(self, command_list):
        command = wrap_with_ssh(tnt_config.INSTANCE_USER, self.get_ip(), command_list)
        return self.executor.execute_async(command)
