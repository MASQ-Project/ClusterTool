# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from config import COMMANDS
from tnt_config import INSTANCES

def _verbose_usage():
    print("available commands:")
    for command in sorted(COMMANDS.keys()):
        COMMANDS[command].display()
    print("only one per line, all lower case")
    print("blank line to exit\n")

def _list_commands():
    print("commands: %s, (blank line to exit)" % COMMANDS.keys())

def _run(user_command):
    for command in COMMANDS.keys():
        if user_command.startswith(command):
            the_input = user_command[len(command):]
            COMMANDS[command].run_for(the_input)
            return
    print("unrecognized command: %s" % user_command)
    _verbose_usage()

def _loop():
    command = raw_input().strip()
    while command != '':
        _run(command)
        print('%s done' % command)
        _list_commands()
        command = raw_input("\n").strip()

def go():
    COMMANDS['init'].run()

    if len(INSTANCES) == 0:
        print("You haven't configured any nodes for this run of TNT. Exiting...")
        return

    COMMANDS['info'].run()

    _verbose_usage()

    while len(INSTANCES) > 0:
        _loop()

        if len(INSTANCES) > 0:
            exit = raw_input("It looks like there are instances still running. Are you sure you want to exit? [y/N] ").strip().lower()
            if exit == 'y':
                return
            print("")
            _list_commands()
            print("")
