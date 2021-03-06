# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function

import tnt_config


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
        index_names = self._cleanse_input(the_input)
        if len(index_names) == 0:
            self.run()

        if 'all' in index_names:
            index_names = tnt_config.INSTANCES.keys()

        self._run_for_all(self.sub_fn, index_names)

    def _choose_instances(self):
        the_input = raw_input("\t%s: choose from %s (space-delimited) or 'all' (blank line to cancel): " % (self.name, sorted(tnt_config.INSTANCES.keys()))).strip()
        # enable exit on blank line
        if the_input == '':
            return ['']

        return self._cleanse_input(the_input)

    def _cleanse_input(self, the_input):
        names = self._split_input(the_input)
        return self._cleanse_names(names)

    def _split_input(self, the_input):
        index_names = the_input.strip().split(' ')
        # eliminate extra inner whitespace and filter out empty strings
        return [index_name.strip() for index_name in index_names if index_name != '']

    def _cleanse_names(self, index_names):
        # eliminate duplicate names
        index_names = set(index_names)
        # check for unknown instances
        for index_name in index_names:
            if index_name not in tnt_config.INSTANCES.keys() and index_name != 'all':
                print("\tno known instance called %s" % index_name)
                return []
        return index_names

    def _choose_and_run(self, fn):
        while True:
            index_names = self._choose_instances()
            if '' in index_names:
                return

            to_return = False
            if 'all' in index_names:
                index_names = tnt_config.INSTANCES.keys()
                to_return = True

            self._run_for_all(fn, index_names)
            if to_return:
                return

    def _run_for_all(self, fn, index_names):
        for index_name in sorted(index_names):
            fn(tnt_config.INSTANCES[index_name])


class SetCommand(SelectCommand):
    def __init__(self):
        SelectCommand.__init__(self, "set", lambda: 0, "sets attributes on a Node before it is started")

    def display(self):
        print(
            "%s> Prompts for instance name then sets an attribute on the instance(s) specified" %
            "\t{0:-<18}".format(self.name)
        )

    def run(self):
        print("run Usage: set <attribute> <value> [ <instance> [ <instance> ... ] ]")

    def run_for(self, the_input):
        input_words = self._split_input(the_input)
        if len(input_words) < 2:
            print("run_for Usage: set <attribute> <value> [ <instance> [ <instance> ... ] ]")
            return
        attribute = input_words.pop(0)
        value = input_words.pop(0)
        names = self._cleanse_names(input_words)
        fn = lambda instance: self._set_attribute(attribute, value, instance)
        if len(names) == 0:
            self._choose_and_run(fn)

        if 'all' in names:
            names = tnt_config.INSTANCES.keys()

        self._run_for_all(fn, names)

    def _set_attribute(self, attribute, value, instance):
        instance.attributes[attribute] = value
