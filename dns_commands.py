# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from abc import ABCMeta, abstractmethod

DNS_UTILITY_COMMAND = "sudo ./dns_utility %s; ./dns_utility status"


class DnsCommands():
    __metaclass__ = ABCMeta

    @abstractmethod
    def dns_utility(self, command): raise NotImplementedError
