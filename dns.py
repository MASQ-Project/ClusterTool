# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function


class Dns:
    def __init__(self, name, dns_commands):
        self.name = name
        self.dns_commands = dns_commands
        self.dns_status = ""

    def subvert(self):
        self._generic("subvert")

    def revert(self):
        self._generic("revert")

    def _generic(self, cmd):
        if self.dns_status == "%sed" % cmd:
            print("%s already %sed" % (self.name, cmd))
            return

        print("\t%sing DNS on %s..." % (cmd, self.name))
        (stdoutdata, stderrdata) = self.dns_commands.dns_utility(cmd)
        self.dns_status = stdoutdata.strip()
        print("\tdone.")
