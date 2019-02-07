# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from command import SelectCommand


def name():
    return 'nfo'


def command():
    return SelectCommand(name(), _nfo, "nukes from orbit - it's the only way to be sure. Restarts")


def _nfo(instance):
    instance.restart()
