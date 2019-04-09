# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from command import InputCommand
from tnt_config import INSTANCES


def name():
    return 'cluster'


def command():
    return InputCommand(name(), _start_cluster, "Starts the specified number of nodes all with the same neighbor")


def _start_cluster(count):
    try:
        iterations_left = int(count)
    except ValueError:
        print("FAILED TO START cluster: %s is not an integer" % count)
        return
    sorted_instances = sorted(INSTANCES.iteritems(), key=lambda (key, value): value.node_id)
    available_instances = filter(lambda (key, value): value.node.descriptor == '', sorted_instances)
    cluster_descriptor = _find_descriptor_by_max_key_of_running_instances(sorted_instances)
    for instance_name, instance in available_instances:
        if iterations_left == 0:
            break

        if cluster_descriptor == '':
            cluster_descriptor = instance.start_node()
        else:
            instance.start_node(cluster_descriptor)
            iterations_left -= 1


def _find_descriptor_by_max_key_of_running_instances(sorted_instances):
    running_instances = filter(lambda (key, value): value.node.descriptor != '', sorted_instances)
    if len(running_instances) == 0:
        return ''
    return running_instances[-1][1].node.descriptor

