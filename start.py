# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from command import SelectCommand
from tnt_config import INSTANCES

def name():
    return 'start'

def command():
    return SelectCommand(name(), _start_node, "starts SubstratumNode on")

def _start_node(instance):
    bootstrap = None
    if 'bootstrap' in INSTANCES.keys():
        bootstrap = INSTANCES['bootstrap']
    if instance.name != 'bootstrap' and bootstrap is not None and bootstrap.node.descriptor != "": # not trying to start node on bootstrap and node is running on bootstrap
        instance.start_node(bootstrap.node.descriptor)
    elif instance.name == 'bootstrap' and bootstrap is not None and bootstrap.node.descriptor == "": # trying to start node on bootstrap and node is not running on bootstrap
        instance.start_node()
    else:
        print("FAILED TO START %s: did you forget about the bootstrap node?" % instance.name)
        print("\t(if you are trying to start the bootstrap node, this means it may already be running)")
