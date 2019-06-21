# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import node_commands as cmd
import tnt_config
from executor import Executor, TerminalExecutor
from ssh_wrapper import wrap_with_ssh
import os


class NodeSshCommands(cmd.NodeCommands):

    def __init__(self, ip_fn):
        self.get_ip = ip_fn
        self.executor = Executor()
        self.terminal_executor = TerminalExecutor(self.executor)

    def start(self, node_args):
        command = [
            "sudo ./SubstratumNode",
            "--dns_servers", node_args["dns_servers"].split(' ')[1],
            "--log_level", node_args["log_level"].split(' ')[1],
            "--data_directory", node_args["data_directory"].split(' ')[1],
            "--ip", node_args["ip"].split(' ')[1],
            "--wallet_address", node_args["wallet_address"].split(' ')[1],
        ]
        if "additional_args" in node_args:
            additional_args = node_args["additional_args"].split(' ')
            command.extend(additional_args)
        command.extend([">", "/dev/null", "2>&1", "&"])
        return self.executor.execute_sync(self._wrap_with_ssh(command))

    def stop(self):
        return self.executor.execute_sync(self._wrap_with_ssh([
            cmd.STOP_COMMAND
        ]))

    def cat_logs(self):
        return self.executor.execute_async(self._wrap_with_ssh([
            cmd.CAT_LOGS_COMMAND
        ]))

    def delete_logs(self):
        return self.executor.execute_sync(self._wrap_with_ssh([
            cmd.DELETE_LOGS_COMMAND
        ]))

    def retrieve_logs(self, destination):
        source = "%s@%s:%s" % (
            tnt_config.INSTANCE_USER, self.get_ip(),
            cmd.SUBSTRATUM_NODE_LOG
        )
        return self.executor.execute_sync(
            self._wrap_with_scp(source, destination)
        )

    def update(self, binary):
        destination = "%s@%s:%s" % (tnt_config.INSTANCE_USER, self.get_ip(), binary)
        return self.executor.execute_sync(
            self._wrap_with_scp(os.path.join('binaries', binary), destination)
        )

    def tail(self):
        return self._execute_in_new_terminal([cmd.TAIL_LOGS_COMMAND])

    def shell(self):
        return self._execute_in_new_terminal([])

    def _execute_in_new_terminal(self, command_list):
        command = self._list_to_string(self._wrap_with_ssh(command_list))
        title = "%s" % self.get_ip()
        wrapper_command = "{0} {1}".format(title, command)
        return self.terminal_executor.execute_in_new_terminal(wrapper_command)

    def _list_to_string(self, command_list):
        seperator = ' '
        return seperator.join(command_list)

    def _wrap_with_ssh(self, command_list):
        return wrap_with_ssh(tnt_config.INSTANCE_USER, self.get_ip(), command_list)

    def _wrap_with_scp(self, source, destination):
        args = ["scp",
                "-oStrictHostKeyChecking=no",
                source,
                destination
                ]
        return args
