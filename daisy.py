# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from command import InputCommand
from tnt_config import INSTANCES


def name():
    return 'daisy'


def command():
    return InputCommand(name(), _start_daisy_chain, "Starts the specified number of nodes in a daisy chain")


def _start_daisy_chain(count):
    try:
        iterations_left = int(count)
    except ValueError:
        print("FAILED TO START daisy chain: %s is not an integer" % count)
        return

    next_descriptor = ''
    for node_name, instance in INSTANCES.iteritems():
        if iterations_left == 0:
            break

        if node_name == 'node-0':
            if instance.node.descriptor == '':
                next_descriptor = instance.start_node()
                print('started node %s' % next_descriptor)
            else:
                next_descriptor = instance.node.descriptor
        else:
            next_descriptor = instance.start_node(next_descriptor)
            print('started %s %s' % (node_name, next_descriptor))
            iterations_left -= 1
