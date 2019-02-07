# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from config import COMMANDS


def test_commands():
    assert COMMANDS['init'].name == "init"
    assert COMMANDS['init'].info == "Configures instances for use during this run of TNT"
    assert COMMANDS['info'].name == "info"
    assert COMMANDS['info'].info == "Prints running instance info"
    assert COMMANDS['update'].name == "update"
    assert COMMANDS['update'].info == "sends updated binaries (from pwd) and then nfo"
    assert COMMANDS['start'].name == "start"
    assert COMMANDS['start'].info == "starts SubstratumNode on"
    assert COMMANDS['tail'].name == "tail"
    assert COMMANDS['tail'].info == "opens terminal(s) to tail -f SubstratumNode logs on"
    assert COMMANDS['subvert'].name == "subvert"
    assert COMMANDS['subvert'].info == "subverts"
    assert COMMANDS['curl'].name == "curl"
    assert COMMANDS['curl'].info == "prompts for URL and curl count, and executes on"
    assert COMMANDS['wget'].name == "wget"
    assert COMMANDS['wget'].info == "wgets traffic on"
    assert COMMANDS['verify'].name == "verify"
    assert COMMANDS['verify'].info == "checks whether traffic was routed for"
    assert COMMANDS['revert'].name == "revert"
    assert COMMANDS['revert'].info == "reverts and cleans up traffic generation on"
    assert COMMANDS['inspect'].name == "inspect"
    assert COMMANDS['inspect'].info == "finds all the DB update logs, prompts for which to display, and displays a graph representing the neighborhood of"
    assert COMMANDS['inbound'].name == "inbound"
    assert COMMANDS['inbound'].info == "finds all the received Gossip, prompts for which to display, and displays a graph representing the Gossip sent to"
    assert COMMANDS['outbound'].name == "outbound"
    assert COMMANDS['outbound'].info == "finds all the sent Gossip, prompts for which to display, and displays a graph representing the Gossip sent from"
    assert COMMANDS['stop'].name == "stop"
    assert COMMANDS['stop'].info == "reverts and stops SubstratumNode on"
    assert COMMANDS['finish'].name == "finish"
    assert COMMANDS['finish'].info == "Prompts for destination dir(should not exist), `stop`(all) then download logs to dst dir for all running instances"
    assert COMMANDS['shell'].name == "shell"
    assert COMMANDS['shell'].info == "opens shell(s) on node instance in terminal window"
    assert COMMANDS['kill'].name == "kill"
    assert COMMANDS['kill'].info == "shuts down"
    assert COMMANDS['nfo'].name == "nfo"
    assert COMMANDS['nfo'].info == "nukes from orbit - it's the only way to be sure. Restarts"


def test_inline_functions(mocker):
    mock_instance = mocker.Mock()
    COMMANDS['tail'].sub_fn(mock_instance)
    mock_instance.tail.assert_called_with()
    COMMANDS['subvert'].sub_fn(mock_instance)
    mock_instance.subvert.assert_called_with()
    COMMANDS['curl'].sub_fn(mock_instance)
    mock_instance.curl.assert_called_with()
    COMMANDS['wget'].sub_fn(mock_instance)
    mock_instance.wget.assert_called_with()
    COMMANDS['verify'].sub_fn(mock_instance)
    mock_instance.verify.assert_called_with()
    COMMANDS['revert'].sub_fn(mock_instance)
    mock_instance.revert.assert_called_with()
    COMMANDS['inspect'].sub_fn(mock_instance)
    mock_instance.inspect.assert_called_with()
    COMMANDS['inbound'].sub_fn(mock_instance)
    mock_instance.inbound.assert_called_with()
    COMMANDS['outbound'].sub_fn(mock_instance)
    mock_instance.outbound.assert_called_with()
    COMMANDS['stop'].sub_fn(mock_instance)
    mock_instance.stop_node.assert_called_with()
    COMMANDS['shell'].sub_fn(mock_instance)
    mock_instance.shell.assert_called_with()
