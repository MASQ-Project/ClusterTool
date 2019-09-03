# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from abc import ABCMeta, abstractmethod


SUBSTRATUM_NODE_LOG = "/tmp/SubstratumNode_rCURRENT.log"
STOP_COMMAND = "pkill SubstratumNode"
CAT_LOGS_COMMAND = "cat /tmp/SubstratumNode_rCURRENT.log"
TAIL_LOGS_COMMAND = "tail -f /tmp/SubstratumNode_rCURRENT.log"
DELETE_LOGS_COMMAND = "sudo rm -f /tmp/SubstratumNode*.log"


class NodeCommands:
    __metaclass__ = ABCMeta

    def __init__(self, ip):
        self.ip = ip

    @abstractmethod
    def start(self, node_args): raise NotImplementedError

    @abstractmethod
    def stop(self): raise NotImplementedError

    @abstractmethod
    def tail(self): raise NotImplementedError

    @abstractmethod
    def retrieve_logs(self, destination): raise NotImplementedError

    @abstractmethod
    def update(self, binary): raise NotImplementedError

    @abstractmethod
    def shell(self): raise NotImplementedError

    @abstractmethod
    def delete_logs(self): raise NotImplementedError

    @abstractmethod
    def cat_logs(self): raise NotImplementedError
