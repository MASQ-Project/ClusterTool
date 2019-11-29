# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from command import SelectCommand
import tnt_config


def name():
    return 'start'


def command():
    return SelectCommand(name(), _start_node, "starts MASQNode on")


def _start_node(instance):
    if 'node-0' in tnt_config.INSTANCES.keys():
        node0 = tnt_config.INSTANCES['node-0']
        node0_is_running = (node0.node.descriptor != '')
        directed_to_start_node0 = (instance.index_name() == 'node-0')
        if (not node0_is_running) and directed_to_start_node0:
            instance.start_node()
        elif node0_is_running and (not directed_to_start_node0):
            instance.start_node(node0.node.descriptor)
        elif node0_is_running and directed_to_start_node0:
            print("It appears that node-0 is already running.")
        else:
            print("FAILED TO START %s: try starting node-0 first." % instance.index_name())
    else:
        print("FAILED TO START other: no node-0 configured.")
