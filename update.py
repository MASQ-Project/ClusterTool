# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from command import SelectCommand


def name():
    return 'update'


def command():
    return SelectCommand(
        name(),
        _update,
        "sends updated binaries (from pwd) and then nfo"
    )


def _update(instance):
    instance.update()
