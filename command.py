# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
from tnt_config import INSTANCES


class Command:
    def __init__(self, name, fn, info):
        self.name = name
        self.run = fn
        self.info = info

    def display(self):
        print("%s> %s" % ("\t{0:-<18}".format(self.name), self.info))

    def run_for(self, the_input):
        if len(the_input) > 0:
            print("%s command does not take input (yet?)" % self.name)
        return self.run()


class InputCommand:
    def __init__(self, name, fn, info):
        self.name = name
        self.run = fn
        self.info = info

    def display(self):
        print("%s> %s" % ("\t{0:-<18}".format(self.name), self.info))

    def run_for(self, the_input):
        return self.run(the_input)


class SelectCommand:
    def __init__(self, name, fn, info):
        self.name = name
        self.info = info
        self.sub_fn = fn

    def display(self):
        print(
            "%s> Prompts for instance name then %s the instance(s) specified" %
            ("\t{0:-<18}".format(self.name), self.info)
        )

    def run(self):
        self._choose_and_run(self.sub_fn)

    def run_for(self, the_input):
        names = self._cleanse_input(the_input)
        if len(names) == 0:
            self.run()

        if 'all' in names:
            names = INSTANCES.keys()

        self._run_for_all(self.sub_fn, names)

    def _choose_instances(self):
        the_input = raw_input("\t%s: choose from %s (space-delimited) or 'all' (blank line to cancel): " % (self.name, sorted(INSTANCES.keys()))).strip()
        # enable exit on blank line
        if the_input == '':
            return ['']

        return self._cleanse_input(the_input)

    def _cleanse_input(self, the_input):
        names = the_input.strip().split(' ')
        # eliminate extra inner whitespace and filter out empty strings
        names = [name.strip() for name in names if name != '']
        # eliminate duplicate names
        names = set(names)
        # check for unknown instances
        for name in names:
            if name not in INSTANCES.keys() and name != 'all':
                print("\tno known instance called %s" % name)
                return []

        return names

    def _choose_and_run(self, fn):
        while True:
            names = self._choose_instances()
            if '' in names:
                return

            to_return = False
            if 'all' in names:
                names = INSTANCES.keys()
                to_return = True

            self._run_for_all(fn, names)
            if to_return:
                return

    def _run_for_all(self, fn, instance_names):
        for instance_name in sorted(instance_names):
            fn(INSTANCES[instance_name])
