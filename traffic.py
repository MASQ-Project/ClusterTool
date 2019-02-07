# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from abc import ABCMeta, abstractmethod


class Traffic():
    __metaclass__ = ABCMeta

    @abstractmethod
    def status(self): raise NotImplementedError

    @abstractmethod
    def cleanup(self, executor): raise NotImplementedError
