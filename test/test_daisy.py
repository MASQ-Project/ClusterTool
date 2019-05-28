# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import daisy as subject


class TestDaisy:

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print', autospec=True)

    @pytest.fixture
    def instances(self, mocker):
        self.mock_node0 = mocker.Mock(autospec=True)
        self.mock_node0.name = 'node-0'
        self.mock_node1 = mocker.Mock(autospec=True)
        self.mock_node1.name = 'node-1'
        self.mock_node2 = mocker.Mock(autospec=True)
        self.mock_node2.name = 'node-2'
        instance_dict = {
            'node-0': self.mock_node0,
            'node-1': self.mock_node1,
            'node-2': self.mock_node2
        }
        mocker.patch.object(subject, 'INSTANCES', instance_dict)

    def test_name(self):
        assert subject.name() == 'daisy'

    def test_command(self):
        real_command = subject.command()

        assert real_command.name == 'daisy'
        assert real_command.info == 'Starts the specified number of nodes in a daisy chain'

    def test_command_when_starting_one_node_and_node_is_running_on_node0(self, instances):
        self.mock_node0.node.descriptor = 'descriptor'
        real_command = subject.command()

        real_command.run_for('1')

        self.mock_node0.start_node.assert_not_called()
        self.mock_node1.start_node.assert_called_with('descriptor')

    def test_command_when_trying_to_start_one_node_and_node_is_not_running_on_node0(self, instances):
        self.mock_node0.node.descriptor = ''
        self.mock_node0.start_node.return_value = 'mock-node-descriptor'
        real_command = subject.command()

        real_command.run_for('1')

        self.mock_node0.start_node.assert_called_with()
        self.mock_node1.start_node.assert_called_with('mock-node-descriptor')

    def test_command_when_starting_multiple_nodes_and_node0_is_running(self, instances):
        self.mock_node0.node.descriptor = 'node-0-descriptor'
        self.mock_node1.start_node.return_value = 'node-1-descriptor'
        real_command = subject.command()

        real_command.run_for('2')

        self.mock_node0.start_node.assert_not_called()
        self.mock_node1.start_node.assert_called_with('node-0-descriptor')
        self.mock_node2.start_node.assert_called_with('node-1-descriptor')

    def test_command_when_starting_multiple_nodes_including_node0(self, instances):
        self.mock_node0.node.descriptor = ''
        self.mock_node0.start_node.return_value = 'node-0-descriptor'
        self.mock_node1.start_node.return_value = 'node-1-descriptor'
        real_command = subject.command()

        real_command.run_for('2')

        self.mock_node0.start_node.assert_called_with()
        self.mock_node1.start_node.assert_called_with('node-0-descriptor')
        self.mock_node2.start_node.assert_called_with('node-1-descriptor')

    def test_command_with_bad_count(self, mocker, printing, instances):
        real_command = subject.command()

        real_command.run_for('bad')

        assert self.mock_print.mock_calls == [
            mocker.call('FAILED TO START daisy chain: bad is not an integer')
        ]
