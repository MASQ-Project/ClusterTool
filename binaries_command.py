# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function

import tnt_config
from command import SelectCommand


class BinariesCommand(SelectCommand):
    def __init__(self):
        SelectCommand.__init__(self, "binaries", lambda: 0, "assigns binaries in /binaries subdirectory to a Node before it is started")

    def display(self):
        print(
            "%s> Prompts for instance name then sets the directory from which the binaries will be drawn for that instance" %
            "\t{0:-<18}".format(self.name)
        )

    def run(self):
        print("run Usage: binaries </binaries subdirectory> [ <instance> [ <instance> ... ] ]")

    def run_for(self, the_input):
        input_words = self._split_input(the_input)
        if len(input_words) < 1:
            print("run_for Usage: binaries </binaries subdirectory> [ <instance> [ <instance> ... ] ]")
            return
        subdir = input_words.pop(0)
        names = self._cleanse_names(input_words)
        fn = lambda instance: self._set_binaries_version(subdir, instance)
        if len(names) == 0:
            self._choose_and_run(fn)

        if 'all' in names:
            names = tnt_config.INSTANCES.keys()

        self._run_for_all(fn, names)

    def _set_binaries_version(self, subdir, instance):
        instance.binaries_version = subdir
