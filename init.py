# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from command import Command
from instance import Instance
from tnt_config import *


def name():
    return 'init'


def command():
    return Command(name(), _init, "Configures instances for use during this run of TNT")


def _init():
# TODO save user choices into a config file (gitignore it)
    # check if there is a previous config file
    # display the settings and prompt user if they'd like to use it or reconfigure
    _print_available_instance_info()

# TODO prompt for automated vs manual
    _automated()
    # while _continue_manual():
    #   pass # this is unfortunately clever. _continue_manual will return False when the user enters a blank line

    for instance in INSTANCES.keys():
        INSTANCES[instance].start()


def _print_available_instance_info():
    print("\nAvailable configured cloud instances:")
    print("\tGoogle: %s" % [it.name for it in COMPUTE_INSTANCES])
    print("\tAmazon: %s" % [it.name for it in EC2_INSTANCES])
    print("\nAvailable configured local instances (probably cannot be used alongside above):")
    print("\tVirtualBox: %s\n" % [it.name for it in VIRTUALBOX_INSTANCES])
    print("\tDocker: %s\n" % [it.name for it in DOCKER_INSTANCES])


def _automated():
    (instance_lists, available_count) = _prompt_for_platform_group()
    if available_count == 0:
        return

    # TODO for coordinating between multiple users of TNT it is important to know which instances are already in use before claiming them
    # proposed `status` command can help with this
    instance_count = _prompt_for_instance_count(available_count)
    if instance_count == 0:
        return

    platform_idx = 0
    for idx in range(instance_count):
        node_id = _determine_id()
        api = instance_lists[platform_idx].pop(0)
        if len(instance_lists[platform_idx]) == 0:
            platform_idx = platform_idx + 1

        # TODO what if the instance is already running? maybe already has MASQNode running on it? (proposed `status` command can help with this)
        instance = Instance(node_id, api)
        INSTANCES[instance.name] = instance
        print("Configured %s on %s (%s)" % (instance.name, api.name, api.__class__))


def _determine_id():
    return len(INSTANCES)


def _prompt_for_platform_group():
    while True:
        group = raw_input("Where would you like TNT to run nodes? ('cloud', 'vbox', 'docker' or blank to cancel) ").strip()
        if group == '':
            return (None, 0)
        if group not in ['cloud', 'vbox', 'docker']:
            print("%s is not a valid platform group. Try again" % group)
        else:
            break

    instance_lists = []
    available_count = 0
    if group == 'cloud':
        available_count = len(COMPUTE_INSTANCES + EC2_INSTANCES)
        if len(COMPUTE_INSTANCES) > 0:
            instance_lists.append(COMPUTE_INSTANCES)
        if len(EC2_INSTANCES) > 0:
            instance_lists.append(EC2_INSTANCES)
    if group == 'vbox':
        available_count = len(VIRTUALBOX_INSTANCES)
        if len(VIRTUALBOX_INSTANCES) > 0:
            instance_lists.append(VIRTUALBOX_INSTANCES)
    if group == 'docker':
        available_count = len(DOCKER_INSTANCES)
        if len(DOCKER_INSTANCES) > 0:
            instance_lists.append(DOCKER_INSTANCES)

    return instance_lists, available_count


def _prompt_for_instance_count(available):
    while True:
        user_count = raw_input("How many instances do you want to use? (1-%i, or 'all', blank to cancel) " % available).strip()
        if user_count == '0' or user_count == '':
            return 0
        if user_count == 'all':
            return available

        try:
            count = int(user_count)
            if count in range(available+1):
                return count
            else:
                print("%i is not in range 1-%i. Try again" % (count, available))
        except:
            print("%s isn't a number. Try again" % user_count)


# TODO: uncomment when we enable manual configuration; also add tests
# def _continue_manual():
#     name = _determine_name()
#     print("Configuring %s..." % name)
#
#     api_list = _prompt_for_platform(name)
#     if len(api_list) == 0:
#         return False
#
#     # TODO prompt for which instances (by name) user wants rather than defaulting to first
#     api = api_list.pop(0)
#     INSTANCES[name] = Instance(name, api)
#     return True


# def _get_platform_list(platform):
#     if platform == 'google':
#         return COMPUTE_INSTANCES
#     if platform == 'amazon':
#         return EC2_INSTANCES
#     if platform == 'vbox':
#         return VIRTUALBOX_INSTANCES
#
#
# def _prompt_for_platform(name):
#     while True:
#         platform = raw_input("Which platform do you want to use for %s? (blank line to cancel without configuring) " % name).lower().strip()
#         if platform not in ['google', 'amazon', 'vbox', '']:
#             print("%s isn't a valid platform. Try again" % platform)
#         elif platform == '':
#             return []
#
#         available_count = len(_get_platform_list(platform))
#
#         if available_count == 0:
#             print("Sorry, all the instances on %s are already assigned for this run. Try again" % platform)
#         else:
#             return _get_platform_list(platform)
