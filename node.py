# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
import re
import pexpect
from graphviz import Source
import instance


class Node:
    def __init__(self, name, node_commands):
        self.name = name
        self.node_commands = node_commands
        self.descriptor = ""

    def start(self, ip, neighbor_info):
        if self.descriptor != "":
            print("it looks like node is already running on %s" % self.name)
        elif neighbor_info == "":
            print("\tstarting node %s..." % self.name)
            self._start_node_with(ip)
            print("\tnode running: %s" % self.descriptor)
        else:
            print("\tstarting node %s..." % self.name)
            self._start_node_with(ip, "--neighbors %s" % neighbor_info)
            print("\tnode running: %s" % self.descriptor)
        return self.descriptor

    def shutdown(self):
        print("\tshutting down node on %s..." % self.name)
        self.node_commands.stop()
        self.descriptor = ""
        print("\tdone.")

    def update(self):
        self.shutdown()
        print("\tSending updated binaries to %s instance" % self.name)
        for executable in instance.BINARIES:
            return_code = self.node_commands.update(executable)
            if return_code != 0:
                print("*** scp failed with code %s ***" % return_code)
        print("\tdone.")

    def _start_node_with(self, ip, arg_str):
        # ensure the first descriptor match will be the current running node
        self._delete_existing_log()
        node_args = {
            'dns_servers': "--dns_servers 1.1.1.1",
            'log_level': "--log_level trace",
            'data_directory': "--data_directory /tmp",
            'ip': "--ip %s" % ip,
            'wallet_address': "--wallet_address %s" % self.earning_wallet(ip),
            'additional_args': arg_str,
        }
        self.node_commands.start(node_args)
        self.descriptor = self._wait_for_descriptor()

    def retrieve_logs(self, to_dir):
        print("\tRetrieving logs from %s instance (%s/SubstratumNode-%s.log)" % (self.name, to_dir, self.name))
        self.node_commands.retrieve_logs("%s/SubstratumNode-%s.log" % (to_dir, self.name))
        print("\tdone.")
        
    def shell(self):
        self.node_commands.shell()

    def tail(self):
        print("\tattempting to tail logs on %s" % self.name)
        self.node_commands.tail()
        print("\tdone")

    def display_neighborhood(self):
        self._handle_dot_graph_interaction('Current database', 'neighborhood', 'Neighborhood DB changes')

    def gossip_received(self):
        self._handle_dot_graph_interaction('Received Gossip', 'received', 'Gossip messages received')

    def gossip_produced(self):
        self._handle_dot_graph_interaction('Sent Gossip', 'sent', 'Gossip messages sent')

    @staticmethod
    def earning_wallet(ip):
        fragment = Node._wallet_fragment(ip)
        return "0x%s%s%s%sEEEEEEEE" % (fragment, fragment, fragment, fragment)  # EEEs for "earning"

    @staticmethod
    def consuming_wallet(ip):
        fragment = Node._wallet_fragment(ip)
        return "0x%s%s%s%sCCCCCCCC" % (fragment, fragment, fragment, fragment)  # CCCs for "consuming"

    @staticmethod
    def _wallet_fragment(ip):
        match = re.search(r"(\d+)\.(\d+)\.(\d+)\.(\d+)", ip)
        octets = [int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))]
        return "%02X%02X%02X%02X" % (octets[0], octets[1], octets[2], octets[3])

    def _handle_dot_graph_interaction(self, log_pattern, filename, prompt_message):
        p = self.node_commands.cat_logs()
        idx = p.expect([pexpect.EOF], timeout=None)
        matcher = re.compile('%s: (?P<dot_graph>digraph db {.*; })' % log_pattern)

        matches = []
        logs = p.before
        match = matcher.search(logs)
        while match is not None:
            matches.append(match)
            logs = logs[match.end():]
            match = matcher.search(logs)

        if len(matches) == 0:
            print("\tCould not find any logs about %s" % prompt_message)
            return

        print("\tThere were %i logs about %s for %s." % (len(matches), prompt_message, self.name))
# TODO move all user interaction stuff out into command files.
        while True:
            user_input = raw_input("\tWhich one do you want to see (1-%i)? (blank line to cancel) " % len(matches)).strip()
            if user_input == '':
                return

            idx = -1
            try:
                idx = int(user_input) - 1
                if idx not in range(len(matches)):
                    print("\n\tInvalid input '%s', please use (1-%i). " % (user_input, len(matches)))
                    continue
            except:
                print("\n\tInvalid input '%s', please use (1-%i). " % (user_input, len(matches)))
                continue

            Source(matches[idx].group('dot_graph'), directory="graphviz", filename="%s-%s-%i" % (self.name, filename, idx+1), format="png").view()

    def _delete_existing_log(self):
        print("\tdeleting previous log on %s..." % self.name)
        self.node_commands.delete_logs()
        print("\tdone.")

    def _wait_for_descriptor(self):
        print("\t\tWaiting for node info...")

        p = self.node_commands.cat_logs()
        idx = p.expect(['.*SubstratumNode local descriptor: (.+)[\t\r\n\v\f ]', pexpect.EOF], timeout=None)

        while idx != 0:
            p = self.node_commands.cat_logs()
            idx = p.expect(['.*SubstratumNode local descriptor: (.+)[\t\r\n\v\f ]', pexpect.EOF], timeout=None)

        descriptor = p.match.group(1).split('\r')[0].strip()
        print("\t\tdone.")
        return descriptor
