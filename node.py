# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
import re
import sys

import pexpect
from graphviz import Source
import instance
import sha3
import tnt_config


class Node:
    def __init__(self, machine_name, node_commands):
        self._machine_name = machine_name
        self.node_commands = node_commands
        self.descriptor = ""
        self.instance = None

    def machine_name(self):
        return self._machine_name

    def start(self, ip, neighbor_descriptors):
        if self.descriptor != "":
            print("it looks like node is already running on %s" % self.machine_name())
            return self.descriptor
        self.instance = self._find_matching_instance()
        if neighbor_descriptors == "":
            print("\tstarting initial node %s..." % self.machine_name())
            self._start_node_with(ip)
            print("\tnode running: %s" % self.descriptor)
        else:
            print("\tstarting debut node %s..." % self.machine_name())
            self._start_node_with(ip, neighbor_descriptors)
            print("\tnode running: %s" % self.descriptor)
        return self.descriptor

    def shutdown(self):
        print("\tshutting down node on %s..." % self.machine_name())
        self.node_commands.stop()
        self.descriptor = ""
        print("\tdone.")

    def update(self):
        self.shutdown()
        print("\tSending updated binaries to %s instance" % self.machine_name())
        for executable in instance.BINARIES:
            return_code = self.node_commands.update(executable)
            if return_code != 0:
                print("*** scp failed with code %s ***" % return_code)
        print("\tdone.")

    def _find_matching_instance(self):
        matching_instances = filter(lambda i: i.machine_name() == self.machine_name(), tnt_config.INSTANCES.values())
        if len(matching_instances) != 1:
            sys.exit("There should have been exactly one instance named %s, not %s" % (self.machine_name(), len(matching_instances)))
        return matching_instances[0]

    def _start_node_with(self, ip, neighbor_descriptors=None):
        # ensure the first descriptor match will be the current running node
        self._delete_existing_log()
        args_map = {
            'dns-servers': '1.1.1.1',
            'log-level': 'trace',
            'data-directory': '/tmp',
            'ip': ip,
            'earning-wallet': self.earning_wallet(ip),
            'consuming-private-key': self.consuming_private_key(ip),
        }
        if neighbor_descriptors:
            args_map['neighbors'] = neighbor_descriptors
        args_map.update(self.instance.attributes)
        self.node_commands.start(args_map)
        self.descriptor = self._wait_for_descriptor()

    def retrieve_logs(self, to_dir):
        print("\tRetrieving logs from %s instance (%s/MASQNode-%s.log)" % (self.machine_name(), to_dir, self.machine_name()))
        self.node_commands.retrieve_logs("%s/MASQNode-%s.log" % (to_dir, self.machine_name()))
        print("\tdone.")
        
    def shell(self):
        self.node_commands.shell()

    def tail(self):
        print("\tattempting to tail logs on %s" % self.machine_name())
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
    def consuming_private_key(ip):
        keccak = sha3.keccak_256()
        keccak.update(ip.encode('utf-8'))
        return keccak.hexdigest()

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

        print("\tThere were %i logs about %s for %s." % (len(matches), prompt_message, self.machine_name()))
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

            Source(matches[idx].group('dot_graph'), directory="graphviz", filename="%s-%s-%i" % (self.machine_name(), filename, idx+1), format="png").view()

    def _delete_existing_log(self):
        print("\tdeleting previous log on %s..." % self.machine_name())
        self.node_commands.delete_logs()
        print("\tdone.")

    def _wait_for_descriptor(self):
        print("\t\tWaiting for node info...")

        p = self.node_commands.cat_logs()
        idx = p.expect(['.*MASQ Node local descriptor: (.+)[\t\r\n\v\f ]', pexpect.EOF], timeout=None)

        while idx != 0:
            p = self.node_commands.cat_logs()
            idx = p.expect(['.*MASQ Node local descriptor: (.+)[\t\r\n\v\f ]', pexpect.EOF], timeout=None)

        descriptor = p.match.group(1).split('\r')[0].strip()
        print("\t\tdone.")
        return descriptor
