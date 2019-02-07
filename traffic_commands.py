# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from abc import ABCMeta, abstractmethod


class TrafficCommands:
    __metaclass__ = ABCMeta

    @abstractmethod
    def curl(self, command_list): raise NotImplementedError

    @abstractmethod
    def wget(self, command_list): raise NotImplementedError

    @abstractmethod
    def cleanup(self, command_list): raise NotImplementedError
