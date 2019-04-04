# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from command import InputCommand


def name():
    return 'help'


def command():
    return InputCommand('help', _prompt_for_usage, "shows usage information for specified command")


def _prompt_for_usage(the_input):
    target = the_input.strip()

    if len(target) < 1:
        target = raw_input("Which command would you like help for? (blank to cancel) ").strip()
    if target != '':
        with open('USAGE.md', 'rt') as usage_fh:
            while True:
                line = usage_fh.readline()
                if line == '':
                    print("\nNo help available for command '%s'\n" % target)
                    return
                if line == '### %s\n' % target:
                    break
            while True:
                line = usage_fh.readline()
                if line == '':
                    break
                if line.startswith('### '):
                    break
                print('%s' % line, end='')
