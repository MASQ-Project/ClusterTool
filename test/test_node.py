# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from node import Node
import pexpect


class TestNode:

    @pytest.fixture
    def node_commands(self, mocker):
        self.mock_node_commands = mocker.Mock()

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print', autospec=True)

    @pytest.fixture
    def graphviz(self, mocker):
        self.mock_graphviz = mocker.patch('node.Source', autospec=True)

    def test_init(self):
        subject = Node('booga', 'node_commands')

        assert subject.name == 'booga'
        assert subject.node_commands == 'node_commands'
        assert subject.descriptor == ''

    def test_start_standard_node_wait_for_descriptor(self, node_commands, printing, mocker):
        subject = Node('booga', self.mock_node_commands)
        self.mock_node_commands.cat_logs.return_value.expect.side_effect = [1, 0]
        self.mock_node_commands.cat_logs.return_value.match.group.return_value.split.return_value = [' descriptor ']

        real_descriptor = subject.start('1.2.3.4', 'neighbor_descriptor')

        assert self.mock_print.mock_calls == [
            mocker.call('\tstarting node booga...'),
            mocker.call('\tdeleting previous log on booga...'),
            mocker.call('\tdone.'),
            mocker.call('\t\tWaiting for node info...'),
            mocker.call('\t\tdone.'),
            mocker.call('\tnode running: descriptor'),
        ]

        self.mock_node_commands.delete_logs.assert_called_with()
        self.mock_node_commands.cat_logs.return_value.expect.assert_called_with(['.*SubstratumNode local descriptor: (.+)[\t\r\n\v\f ]', pexpect.EOF], timeout=None)
        self.mock_node_commands.cat_logs.return_value.match.group.assert_called_with(1)
        self.mock_node_commands.cat_logs.return_value.match.group.return_value.split.assert_called_with('\r')
        self.mock_node_commands.start.assert_called_with({
            'dns-servers': "--dns-servers 1.1.1.1",
            'log-level': "--log-level trace",
            'data-directory': "--data-directory /tmp",
            'ip': "--ip 1.2.3.4",
            'earning-wallet': "--earning-wallet 0x01020304010203040102030401020304EEEEEEEE",
            'consuming-private-key': '--consuming-private-key 89d59b93ef6a94c977e1812b727d5f123f7d825ab636e83aad3e2845a68eaedb',
            'additional-args': "--neighbors neighbor_descriptor",
        })
        assert real_descriptor == 'descriptor'

    def test_start_node_without_neighbors_wait_for_descriptor(self, node_commands, printing, mocker):
        subject = Node('booga', self.mock_node_commands)
        self.mock_node_commands.cat_logs.return_value.expect.side_effect = [1, 0]
        self.mock_node_commands.cat_logs.return_value.match.group.return_value.split.return_value = [' descriptor ']

        real_descriptor = subject.start('1.2.3.4', "")

        assert self.mock_print.mock_calls == [
            mocker.call('\tstarting node booga...'),
            mocker.call('\tdeleting previous log on booga...'),
            mocker.call('\tdone.'),
            mocker.call('\t\tWaiting for node info...'),
            mocker.call('\t\tdone.'),
            mocker.call('\tnode running: descriptor'),
        ]

        self.mock_node_commands.delete_logs.assert_called_with()
        self.mock_node_commands.cat_logs.return_value.expect.assert_called_with(['.*SubstratumNode local descriptor: (.+)[\t\r\n\v\f ]', pexpect.EOF], timeout=None)
        self.mock_node_commands.cat_logs.return_value.match.group.assert_called_with(1)
        self.mock_node_commands.cat_logs.return_value.match.group.return_value.split.assert_called_with('\r')
        self.mock_node_commands.start.assert_called_with({
            'dns-servers': "--dns-servers 1.1.1.1",
            'log-level': "--log-level trace",
            'data-directory': "--data-directory /tmp",
            'ip': "--ip 1.2.3.4",
            'earning-wallet': "--earning-wallet 0x01020304010203040102030401020304EEEEEEEE",
            'consuming-private-key': '--consuming-private-key 89d59b93ef6a94c977e1812b727d5f123f7d825ab636e83aad3e2845a68eaedb',
        })
        assert real_descriptor == 'descriptor'

    def test_start_when_already_started(self, node_commands, printing, mocker):
        subject = Node('booga', self.mock_node_commands)
        subject.descriptor = 'descriptor'

        real_descriptor = subject.start('1.2.3.4', '')

        assert self.mock_print.mock_calls == [
            mocker.call('it looks like node is already running on booga')
        ]
        assert real_descriptor == 'descriptor'

    def test_shutdown(self, node_commands, printing, mocker):
        subject = Node('booga', self.mock_node_commands)
        subject.descriptor = 'not_blanked'

        subject.shutdown()

        assert self.mock_print.mock_calls == [
            mocker.call('\tshutting down node on booga...'),
            mocker.call('\tdone.')
        ]
        self.mock_node_commands.stop.assert_called_with()
        assert subject.descriptor == ''

    def test_update_successfully(self, node_commands, printing, mocker):
        subject = Node('booga', self.mock_node_commands)
        subject.descriptor = 'not_blanked'
        self.mock_node_commands.update.return_value = 0

        subject.update()

        assert self.mock_print.mock_calls == [
            mocker.call('\tshutting down node on booga...'),
            mocker.call('\tdone.'),
            mocker.call('\tSending updated binaries to booga instance'),
            mocker.call('\tdone.')
        ]
        self.mock_node_commands.stop.assert_called_with()
        assert subject.descriptor == ''
        assert self.mock_node_commands.update.mock_calls == [
            mocker.call("SubstratumNode"),
            mocker.call("dns_utility")
        ]

    def test_update_failure(self, node_commands, printing, mocker):
        subject = Node('booga', self.mock_node_commands)
        subject.descriptor = 'not_blanked'
        self.mock_node_commands.update.return_value = 1

        subject.update()

        assert self.mock_print.mock_calls == [
            mocker.call('\tshutting down node on booga...'),
            mocker.call('\tdone.'),
            mocker.call('\tSending updated binaries to booga instance'),
            mocker.call('*** scp failed with code 1 ***'),
            mocker.call('*** scp failed with code 1 ***'),
            mocker.call('\tdone.')
        ]
        self.mock_node_commands.stop.assert_called_with()
        assert subject.descriptor == ''

    def test_retrieve_logs(self, printing, mocker, node_commands):
        subject = Node('booga', self.mock_node_commands)

        subject.retrieve_logs("to_dir")

        assert self.mock_print.mock_calls == [
            mocker.call('\tRetrieving logs from booga instance (to_dir/SubstratumNode-booga.log)'),
            mocker.call('\tdone.')
        ]
        self.mock_node_commands.retrieve_logs.assert_called_with('to_dir/SubstratumNode-booga.log')

    def test_shell(self, node_commands):
        subject = Node('booga', self.mock_node_commands)

        subject.shell()

        self.mock_node_commands.shell.assert_called_with()

    def test_tail(self, node_commands, printing, mocker):
        subject = Node('booga', self.mock_node_commands)

        subject.tail()

        assert self.mock_print.mock_calls == [
            mocker.call('\tattempting to tail logs on booga'),
            mocker.call('\tdone')
        ]
        self.mock_node_commands.tail.assert_called_with()

    def test_display_neighborhood(self, node_commands, printing, graphviz, mocker):
        subject = Node('booga', self.mock_node_commands)
        self.mock_node_commands.cat_logs.return_value.before = 'Current database: digraph db {...; }'
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['1', '']

        subject.display_neighborhood()

        self.mock_node_commands.cat_logs.return_value.expect.assert_called_with(
            [pexpect.EOF], timeout=None
        )

        assert self.mock_print.mock_calls == [
            mocker.call('\tThere were 1 logs about Neighborhood DB changes for booga.')
        ]
        assert mock_input.mock_calls == [
            mocker.call('\tWhich one do you want to see (1-1)? (blank line to cancel) '),
            mocker.call('\tWhich one do you want to see (1-1)? (blank line to cancel) ')
        ]
        self.mock_graphviz.assert_called_with('digraph db {...; }', directory="graphviz", filename="booga-neighborhood-1", format="png")
        self.mock_graphviz.return_value.view.assert_called_with()

    def test_display_neighborhood_when_no_logs_found(self, node_commands, printing, graphviz, mocker):
        subject = Node('booga', self.mock_node_commands)
        self.mock_node_commands.cat_logs.return_value.before = ''
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['1', '']

        subject.display_neighborhood()

        self.mock_node_commands.cat_logs.return_value.expect.assert_called_with(
            [pexpect.EOF], timeout=None
        )

        assert self.mock_print.mock_calls == [
            mocker.call('\tCould not find any logs about Neighborhood DB changes')
        ]

    def test_gossip_received(self, node_commands, printing, graphviz, mocker):
        subject = Node('booga', self.mock_node_commands)
        self.mock_node_commands.cat_logs.return_value.before = 'Received Gossip: digraph db {...; }'
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['1', '']

        subject.gossip_received()

        self.mock_node_commands.cat_logs.return_value.expect.assert_called_with(
            [pexpect.EOF], timeout=None
        )

        assert self.mock_print.mock_calls == [
            mocker.call('\tThere were 1 logs about Gossip messages received for booga.')
        ]
        assert mock_input.mock_calls == [
            mocker.call('\tWhich one do you want to see (1-1)? (blank line to cancel) '),
            mocker.call('\tWhich one do you want to see (1-1)? (blank line to cancel) ')
        ]
        self.mock_graphviz.assert_called_with('digraph db {...; }', directory="graphviz", filename="booga-received-1", format="png")
        self.mock_graphviz.return_value.view.assert_called_with()

    def test_gossip_produced(self, node_commands, printing, graphviz, mocker):
        subject = Node('booga', self.mock_node_commands)
        self.mock_node_commands.cat_logs.return_value.before = 'Sent Gossip: digraph db {...; }'
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['1', '']

        subject.gossip_produced()

        self.mock_node_commands.cat_logs.return_value.expect.assert_called_with(
            [pexpect.EOF], timeout=None
        )

        assert self.mock_print.mock_calls == [
            mocker.call('\tThere were 1 logs about Gossip messages sent for booga.')
        ]
        assert mock_input.mock_calls == [
            mocker.call('\tWhich one do you want to see (1-1)? (blank line to cancel) '),
            mocker.call('\tWhich one do you want to see (1-1)? (blank line to cancel) ')
        ]
        self.mock_graphviz.assert_called_with('digraph db {...; }', directory="graphviz", filename="booga-sent-1", format="png")
        self.mock_graphviz.return_value.view.assert_called_with()

    def test_display_neighborhood_when_invalid_input(self, node_commands, printing, graphviz, mocker):
        subject = Node('booga', self.mock_node_commands)
        self.mock_node_commands.cat_logs.return_value.before = 'Current database: digraph db {...; }'
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['2', 'not_a_number', '']

        subject.display_neighborhood()

        self.mock_node_commands.cat_logs.return_value.expect.assert_called_with(
            [pexpect.EOF], timeout=None
        )

        assert self.mock_print.mock_calls == [
            mocker.call('\tThere were 1 logs about Neighborhood DB changes for booga.'),
            mocker.call("\n\tInvalid input '2', please use (1-1). "),
            mocker.call("\n\tInvalid input 'not_a_number', please use (1-1). ")
        ]
        assert mock_input.mock_calls == [
            mocker.call('\tWhich one do you want to see (1-1)? (blank line to cancel) '),
            mocker.call('\tWhich one do you want to see (1-1)? (blank line to cancel) '),
            mocker.call('\tWhich one do you want to see (1-1)? (blank line to cancel) ')
        ]
        assert self.mock_graphviz.return_value.view.call_count == 0
