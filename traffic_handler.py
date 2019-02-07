# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from __future__ import print_function
import time
from wget import Wget
from curl import Curl

WGET_SITES = [
    "google.com",
    "youtube.com",
    "wikipedia.org",
    "reddit.com",
    "yahoo.com",
    "amazon.com",
]

CURL_SITE = "https://www.piday.org/million/"


class TrafficHandler():
    def __init__(self, name, traffic_commands):
        self.name = name
        self.traffic_commands = traffic_commands
        self.traffic_handles = []

    def curl(self, curl_what=CURL_SITE):
        # TODO prompt for the url, default if none given
        if self.name == 'bootstrap':
            return
        # TODO move all user interaction stuff out into command files.
        curl_count = -1
        while curl_count < 0:
            user_count = raw_input(
                "How many curls for %s? (blank line to cancel) " %
                self.name
            ).strip()
            if user_count == "":
                return
            try:
                curl_count = int(user_count)
            except ValueError:
                print("%s is not a number" % user_count)
                continue
            if curl_count < 0:
                print("%i is not a valid number" % curl_count)

        print("\tstarting curl on %s..." % self.name)
        for idx in range(curl_count):
            print("%s sending curl %s #%i" % (time.ctime(), curl_what, idx))
            self.traffic_handles.append(
                Curl(curl_what, self.traffic_commands.curl)
            )
            time.sleep(2)
        print("\tdone.")

    def wget(self):
        if self.name == 'bootstrap':
            return

        print("\tstarting traffic on %s..." % self.name)
        for site in WGET_SITES:
            print("%s sending wget %s" % (time.ctime(), site))
            self.traffic_handles.append(Wget(site, self.traffic_commands.wget))
            time.sleep(2)
        print("\tdone.")

    def stop(self):
        if self.name == 'bootstrap':
            return

        for traffic_handle in self.traffic_handles:
            traffic_handle.cleanup(self.traffic_commands.cleanup)

        self.traffic_handles = []
        print("\tdone.")

    def verify(self):
        if self.name == 'bootstrap':
            return

        elif len(self.traffic_handles) == 0:
            print("\tyou didn't request traffic on %s" % self.name)
            return

        for traffic_handle in self.traffic_handles:
            print("%s - %s" % (self.name, traffic_handle.status()))

        print("")
