# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from node_commands import *


class TestNodeCommands:

    def test_constants(self):
        assert SUBSTRATUM_NODE_LOG == '/tmp/SubstratumNode_rCURRENT.log'
        assert STOP_COMMAND == 'pkill SubstratumNode'
        assert CAT_LOGS_COMMAND == 'cat /tmp/SubstratumNode_rCURRENT.log'
        assert TAIL_LOGS_COMMAND == 'tail -f /tmp/SubstratumNode_rCURRENT.log'
        assert DELETE_LOGS_COMMAND == 'sudo rm -f /tmp/SubstratumNode*.log'
