# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from abc import ABCMeta, abstractmethod


MASQ_NODE_LOG = "/tmp/MASQNode_rCURRENT.log"
STOP_COMMAND = "pkill MASQNode"
CAT_LOGS_COMMAND = "cat /tmp/MASQNode_rCURRENT.log"
TAIL_LOGS_COMMAND = "tail -f /tmp/MASQNode_rCURRENT.log"
DELETE_LOGS_COMMAND = "sudo rm -f /tmp/MASQNode*.log"


class NodeCommands:
    __metaclass__ = ABCMeta

    def __init__(self, ip):
        self.ip = ip

    @abstractmethod
    def start(self, args_map, binaries_version): raise NotImplementedError

    @abstractmethod
    def stop(self): raise NotImplementedError

    @abstractmethod
    def tail(self): raise NotImplementedError

    @abstractmethod
    def retrieve_logs(self, destination): raise NotImplementedError

    @abstractmethod
    def update(self, binary, binaries_version): raise NotImplementedError

    @abstractmethod
    def shell(self): raise NotImplementedError

    @abstractmethod
    def delete_logs(self): raise NotImplementedError

    @abstractmethod
    def cat_logs(self): raise NotImplementedError
