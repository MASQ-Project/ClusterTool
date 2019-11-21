# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from command import SelectCommand
from tnt_config import *
from compute import Compute
from ec2 import EC2
from virtualbox import VirtualBoxManage
from docker import Docker


def name():
    return 'kill'


def command():
    return SelectCommand(name(), _kill, "shuts down")


def _kill(instance):
    instance_name = instance.index_name()
    api = instance.instance_api
    instance.kill()

    del INSTANCES[instance_name]

    if isinstance(api, EC2):
        EC2_INSTANCES.append(api)
    elif isinstance(api, Compute):
        COMPUTE_INSTANCES.append(api)
    elif isinstance(api, VirtualBoxManage):
        VIRTUALBOX_INSTANCES.append(api)
    elif isinstance(api, Docker):
        DOCKER_INSTANCES.append(api)
