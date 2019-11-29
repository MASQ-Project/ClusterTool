# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from command import SelectCommand
from compute import Compute
from ec2 import EC2
from virtualbox import VirtualBoxManage
from docker import Docker
import tnt_config


def name():
    return 'kill'


def command():
    return SelectCommand(name(), _kill, "shuts down")


def _kill(instance):
    instance_name = instance.index_name()
    api = instance.instance_api
    instance.kill()

    del tnt_config.INSTANCES[instance_name]

    if isinstance(api, EC2):
        tnt_config.EC2_INSTANCES.append(api)
    elif isinstance(api, Compute):
        tnt_config.COMPUTE_INSTANCES.append(api)
    elif isinstance(api, VirtualBoxManage):
        tnt_config.VIRTUALBOX_INSTANCES.append(api)
    elif isinstance(api, Docker):
        tnt_config.DOCKER_INSTANCES.append(api)
