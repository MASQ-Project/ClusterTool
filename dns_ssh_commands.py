# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import tnt_config
from dns_commands import *
from executor import Executor
from ssh_wrapper import wrap_with_ssh


class DnsSshCommands(DnsCommands):
    def __init__(self, ip_fn):
        self.executor = Executor()
        self.get_ip = ip_fn
        
    def dns_utility(self, command):
        return self.executor.execute_sync_with_output(self._wrap_with_ssh([DNS_UTILITY_COMMAND % command]))

    def _wrap_with_ssh(self, command_list):
        return wrap_with_ssh(tnt_config.INSTANCE_USER, self.get_ip(), command_list)
