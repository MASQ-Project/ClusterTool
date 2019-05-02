# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
import pexpect
import subprocess as sp
import sys
import os
import shutil


class Executor:

    def execute_sync(self, command_list):
        return sp.call(command_list)

    def execute_async(self, command_list):
        return pexpect.spawn(command_list[0], command_list[1:])

    def execute_sync_with_output(self, command_list):
        return sp.Popen(command_list, stdout=sp.PIPE, stderr=sp.PIPE).communicate()


class TerminalExecutor:
    
    def __init__(self, executor):
        self.executor = executor

    def execute_in_new_terminal(self, command=""):
        if sys.platform not in _NEW_TERMINAL_BY_PLATFORM.keys():
            print("\tThis TNT command is not yet supported on the current platform (%s)" % sys.platform)
            return
        args = _NEW_TERMINAL_BY_PLATFORM[sys.platform](command)
        return self.executor.execute_sync(args)


def _scriptify(command):
    filename = '/tmp/tnt_terminal.sh'
    with open(filename, 'w') as f:
        f.write(command)
    os.chmod(filename, 0755)
    return filename

def _shell_wrap(command):
    source = './tnt_wrapper.sh'
    destination = '/tmp/tnt_wrapper.sh'
    shutil.copyfile(source, destination)
    os.chmod(destination, 0755)
    wrapped_command = "\"{0}\" {1}".format(destination, command)
    return wrapped_command


_NEW_TERMINAL_BY_PLATFORM = {
    'darwin': lambda command: ['open', '-n', '-a', 'iTerm', '--args'] + [_scriptify(_shell_wrap(command))],
    'linux2': lambda command: ['gnome-terminal', '--geometry', '180x24+0+0', '-e'] + [_scriptify(_shell_wrap(command))],
}
