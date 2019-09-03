# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from command import SelectCommand
from tnt_config import INSTANCES


def name():
    return 'start'


def command():
    return SelectCommand(name(), _start_node, "starts SubstratumNode on")


def _start_node(instance):
    node0 = None
    if 'node-0' in INSTANCES.keys():
        node0 = INSTANCES['node-0']
    if instance.name != 'node-0' and node0 is not None and node0.node.descriptor != "":
        instance.start_node(node0.node.descriptor)
    elif instance.name == 'node-0' and node0 is not None and node0.node.descriptor == "":
        instance.start_node()
    else:
        print("FAILED TO START %s: did you forget about node-0?" % instance.name)
        print("\t(if you are trying to start node-0, this means it may already be running)")
