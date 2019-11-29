# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from node_commands import *


class TestNodeCommands:

    def test_constants(self):
        assert MASQ_NODE_LOG == '/tmp/MASQNode_rCURRENT.log'
        assert STOP_COMMAND == 'pkill MASQNode'
        assert CAT_LOGS_COMMAND == 'cat /tmp/MASQNode_rCURRENT.log'
        assert TAIL_LOGS_COMMAND == 'tail -f /tmp/MASQNode_rCURRENT.log'
        assert DELETE_LOGS_COMMAND == 'sudo rm -f /tmp/MASQNode*.log'
