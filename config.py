# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from command import SelectCommand
import finish, info, init, nfo, update, kill, start, help, daisy

COMMANDS = {
    init.name(): init.command(),  # setup
    info.name(): info.command(),  # always "all"
    update.name(): update.command(),
    start.name(): start.command(),
    'tail': SelectCommand('tail', lambda instance: instance.tail(), "opens terminal(s) to tail -f SubstratumNode logs on"),
    'subvert': SelectCommand('subvert', lambda instance: instance.subvert(), "subverts"),
    'curl': SelectCommand('curl', lambda instance: instance.curl(), "prompts for URL and curl count, and executes on"),
    'wget': SelectCommand('wget', lambda instance: instance.wget(), "wgets traffic on"),
    'verify': SelectCommand('verify', lambda instance: instance.verify(), "checks whether traffic was routed for"),
    'revert': SelectCommand('revert', lambda instance: instance.revert(), "reverts and cleans up traffic generation on"),
    'inspect': SelectCommand('inspect', lambda instance: instance.inspect(), "finds all the DB update logs, prompts for which to display, and displays a graph representing the neighborhood of"),
    'inbound': SelectCommand('inbound', lambda instance: instance.inbound(), "finds all the received Gossip, prompts for which to display, and displays a graph representing the Gossip sent to"),
    'outbound': SelectCommand('outbound', lambda instance: instance.outbound(), "finds all the sent Gossip, prompts for which to display, and displays a graph representing the Gossip sent from"),
    'stop': SelectCommand('stop', lambda instance: instance.stop_node(), "reverts and stops SubstratumNode on"),
    finish.name(): finish.command(), # always "all"
    'shell': SelectCommand('shell', lambda instance: instance.shell(), "opens shell(s) on node instance in terminal window"),
    kill.name(): kill.command(),
    nfo.name(): nfo.command(),
    help.name(): help.command(),
    daisy.name(): daisy.command()

    # TODO status command (finds out which instances are running (checks all platforms), for running instances, determines if node is running on them, if they are subverted, etc)
    # it should not load this state into INSTANCES automatically (multiple pairs could be using different cloud instances, so this should enable coordination)
    # status could prompt for which ones we want to claim for this run of TNT, and load only those into INSTANCES.

    # TODO help command with more detailed command info
}
