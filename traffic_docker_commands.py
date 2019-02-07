# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from traffic_commands import TrafficCommands
from executor import Executor


class TrafficDockerCommands(TrafficCommands):
    def __init__(self, name):
        self.name = name
        self.executor = Executor()

    def wget(self, command_list):
        command = self._wrap_with_docker(command_list)
        return self.executor.execute_async(command)

    def curl(self, command_list):
        command = self._wrap_with_docker(command_list)
        return self.executor.execute_async(command)

    def cleanup(self, command_list):
        command = self._wrap_with_docker(command_list)
        return self.executor.execute_sync(command)

    def _wrap_with_docker(self, command_list):
        command = [
            "docker", "exec", "-it", "--workdir", "/node_root/node/", self.name
        ]
        command.extend(command_list)
        return command
