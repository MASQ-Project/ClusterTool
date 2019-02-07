# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
# Common config/TNT state
INSTANCES = {}
INSTANCE_USER = ''

# CLOUD CONFIGS

# Google Compute config
COMPUTE_CONFIG = {
    'project': '',
    'zone': '',
}

from compute import Compute as Google
COMPUTE_INSTANCES = []


# Amazon EC2 config
EC2_CONFIG = {
    'region': ''
}

from ec2 import EC2 as Amazon
EC2_INSTANCES = []


# LOCAL CONFIGS
# can't (easily) be used alongside cloud APIs until "originating only" nodes are a thing

# VirtualBox config
from virtualbox import VirtualBoxManage as VBox
VIRTUALBOX_INSTANCES = []


from docker import Docker
import json


def get_docker_instances():
    with open('pokemon_name.json', 'r') as pokemon_names:
        data = pokemon_names.read()

    names = json.loads(data)

    index = 2
    instances = []
    for name in names:
        instances.extend([Docker(name, index)])
        index += 1
    return instances[0:253]


DOCKER_INSTANCES = get_docker_instances()
