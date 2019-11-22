# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from command import Command
import tnt_config


def name():
    return 'info'


def command():
    return Command('info', _print_info, "Prints running instance info")


def _print_info():
    for name in sorted(tnt_config.INSTANCES.keys()):
        instance = tnt_config.INSTANCES[name]
        # TODO this will wait forever (not blow up) if the instance is not running... check first!
        print("%s @ %s (%s)" % (name, instance.get_ip(), instance.instance_api.__class__))
