# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from traffic import Traffic
import pexpect

EXIT_CODES = [
    "No problems occurred.",
    "Generic error code.",
    "Parse error---for instance, when parsing command-line options, the .wgetrc or .netrc...",
    "File I/O error.",
    "Network failure.",
    "SSL verification failure.",
    "Username/password authentication failure.",
    "Protocol errors.",
    "Server issued an error response.",
]

FAKE_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"


class Wget(Traffic):
    def __init__(self, site, executor):
        self.site = site
        self.p = executor(self._command())
        self.done = False
        self.result = ""
        self.success_pattern = "HTTP request sent, awaiting response... 200 OK"

    def status(self):
        if self.done:  # we were already done and queried
            return self.result

        if self.p.isalive():  # we are still executing
            if self.p.expect([
                self.success_pattern,
                pexpect.TIMEOUT,
                pexpect.EOF
            ], timeout=1) == 0:
                return "wget %s traffic was successfully routed and is still running" % self.site
            else:
                return "wget %s is still waiting for its first response" % self.site

        # we finished since the last status check
        self.done = True

        # add exit code info
        if self.p.exitstatus < len(EXIT_CODES):
            self.result = "wget %s (%i: %s)" % (
                self.site,
                self.p.exitstatus,
                EXIT_CODES[self.p.exitstatus]
            )
        else:
            self.result = "wget %s (%i: unknown)" % (
                self.site,
                self.p.exitstatus
            )

        # add pass/fail info
        if self.p.exitstatus == 0:
            self.result = "%s %s" % (self.result, "SUCCEEDED")
        else:
            self.result = "%s %s" % (self.result, "FAILED")

        return self.result

    def cleanup(self, executor):
        self.p.terminate(force=True)
        executor(["rm -rf", "/tmp/wget/%s" % self.site])

    def _command(self):
        return [
            "wget", "--directory-prefix=/tmp/wget/", "--page-requisites",
            "--delete-after", self.site,
            "--user-agent='%s'" % FAKE_USER_AGENT, "--no-check-certificate",
            # "--recursive", "--level 0",
            # TODO: recursing takes forever on reddit...
            #      maybe this can be an option for future enhancement
        ]
