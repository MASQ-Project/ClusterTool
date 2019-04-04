# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from command import InputCommand
from tnt_config import INSTANCES


def name():
    return 'cluster'


def command():
    return InputCommand(name(), _start_cluster, "Starts the specified number of nodes all with the same neighbor")


def _start_cluster(count):
    iterations_left = int(count)
    print(INSTANCES)
    sorted_instances = sorted(INSTANCES.iteritems(), key=lambda (key, value): value.node_id)
    print(sorted_instances)
    for instance_name, instance in sorted_instances:
        if iterations_left == 0:
            break

        if instance_name == 'bootstrap':
            instance.start_node()
        else:
            instance.start_node('descriptor')
            iterations_left -= 1
