# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
import os

from command import Command, SelectCommand


def name():
    return 'finish'


def command():
    return Command(name(), _finish_test, "Prompts for destination dir(should not exist), `stop`(all) then download logs to dst dir for all running instances")


def _finish_test():
    prompt = True
    dst_dir = ""
    while prompt:
        dst_dir = raw_input("\tPlease enter a new directory name for the logs (blank line to cancel): ").strip()
        if ' ' in dst_dir:
            print("\tERROR please no spaces, try again\n")
            prompt = True
        elif os.path.exists(dst_dir):
            print("\tERROR %s already exists, try again\n" % dst_dir)
            prompt = True
        else:
            prompt = False

    if dst_dir == '':
        return

    os.mkdir(dst_dir)
    SelectCommand('internal', lambda instance: _finish_instance(instance, dst_dir), 'internal').run_for('all')


def _finish_instance(instance, dst_dir):
    instance.stop_node()
    instance.retrieve_logs(dst_dir)
