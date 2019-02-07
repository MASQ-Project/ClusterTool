# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from command import Command
from tnt_config import INSTANCES


def name():
    return 'info'


def command():
    return Command('info', _print_info, "Prints running instance info")


def _print_info():
    for name in sorted(INSTANCES.keys()):
        instance = INSTANCES[name]
        # TODO this will wait forever (not blow up) if the instance is not running... check first!
        print("%s @ %s (%s)" % (name, instance.get_ip(), instance.instance_api.__class__))
