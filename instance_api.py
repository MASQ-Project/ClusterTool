# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from abc import ABCMeta, abstractmethod, abstractproperty


class InstanceApi:
    __metaclass__ = ABCMeta

    def machine_name(self):
        return self._machine_name

    def getnode(self): raise NotImplementedError

    def setnode(self, value): raise NotImplementedError
    node = abstractproperty(getnode, setnode)

    def getdns(self): raise NotImplementedError

    def setdns(self): raise NotImplementedError
    dns = abstractproperty(getdns, setdns)

    def gettraffic(self): raise NotImplementedError

    def settraffic(self): raise NotImplementedError
    traffic = abstractproperty(gettraffic, settraffic)

    @abstractmethod
    def start_instance(self): raise NotImplementedError

    @abstractmethod
    def stop_instance(self): raise NotImplementedError

    @abstractmethod
    def restart_instance(self): raise NotImplementedError

    @abstractmethod
    def get_external_ip(self): raise NotImplementedError

    # TODO add this fn
    # @abstractmethod
    # def is_running(self): raise NotImplementedError
