# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import cluster as subject


class TestCluster:

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print', autospec=True)

    @pytest.fixture
    def instances(self, mocker):
        self.mock_bootstrap_instance = mocker.Mock(autospec=True)
        self.mock_bootstrap_instance.name = 'bootstrap'
        self.mock_bootstrap_instance.node_id = 0
        self.mock_node1 = make_mock_node(1, mocker)
        self.mock_node2 = make_mock_node(2, mocker)
        self.mock_node3 = make_mock_node(3, mocker)
        self.mock_node4 = make_mock_node(4, mocker)
        self.mock_node5 = make_mock_node(5, mocker)
        self.mock_node6 = make_mock_node(6, mocker)
        self.mock_node7 = make_mock_node(7, mocker)

        instance_dict = {
            'bootstrap': self.mock_bootstrap_instance,
            'node-1': self.mock_node1,
            'node-2': self.mock_node2,
            'node-3': self.mock_node3,
            'node-4': self.mock_node4,
            'node-5': self.mock_node5,
            'node-6': self.mock_node6,
            'node-7': self.mock_node7
        }
        mocker.patch.object(subject, 'INSTANCES', instance_dict)

    def test_name(self):
        assert subject.name() == 'cluster'

    def test_command(self):
        real_command = subject.command()

        assert real_command.name == 'cluster'
        assert real_command.info == 'Starts the specified number of nodes all with the same neighbor'

    def test_command_for_three_nodes_and_bootstrap_is_not_running(self, instances):
        self.mock_bootstrap_instance.node.descriptor = ''
        self.mock_bootstrap_instance.start_node.return_value = 'descriptor'

        real_command = subject.command()

        real_command.run_for('3')

        self.mock_bootstrap_instance.start_node.assert_called_with()
        self.mock_node1.start_node.assert_called_with('descriptor')
        self.mock_node2.start_node.assert_called_with('descriptor')
        self.mock_node3.start_node.assert_called_with('descriptor')
        self.mock_node4.start_node.assert_not_called()
    #
    # def test_command_when_trying_to_start_one_node_and_node_is_not_running_on_bootstrap(self, instances):
    #     self.mock_bootstrap_instance.node.descriptor = ''
    #     self.mock_bootstrap_instance.start_node.return_value = 'mock-node-descriptor'
    #     real_command = subject.command()
    #
    #     real_command.run_for('1')
    #
    #     self.mock_bootstrap_instance.start_node.assert_called_with()
    #     self.mock_node1.start_node.assert_called_with('mock-node-descriptor')
    #
    # def test_command_when_starting_multiple_nodes_and_bootstrap_is_running(self, instances):
    #     self.mock_bootstrap_instance.node.descriptor = 'bootstrap-descriptor'
    #     self.mock_node1.start_node.return_value = 'node-1-descriptor'
    #     real_command = subject.command()
    #
    #     real_command.run_for('2')
    #
    #     self.mock_bootstrap_instance.start_node.assert_not_called()
    #     self.mock_node1.start_node.assert_called_with('bootstrap-descriptor')
    #     self.mock_node2.start_node.assert_called_with('node-1-descriptor')
    #
    # def test_command_when_starting_multiple_nodes_including_bootstrap(self, instances):
    #     self.mock_bootstrap_instance.node.descriptor = ''
    #     self.mock_bootstrap_instance.start_node.return_value = 'bootstrap-descriptor'
    #     self.mock_node1.start_node.return_value = 'node-1-descriptor'
    #     real_command = subject.command()
    #
    #     real_command.run_for('2')
    #
    #     self.mock_bootstrap_instance.start_node.assert_called_with()
    #     self.mock_node1.start_node.assert_called_with('bootstrap-descriptor')
    #     self.mock_node2.start_node.assert_called_with('node-1-descriptor')
    #
    # def test_command_with_bad_count(self, mocker, printing, instances):
    #     real_command = subject.command()
    #
    #     real_command.run_for('bad')
    #
    #     assert self.mock_print.mock_calls == [
    #         mocker.call('FAILED TO START daisy chain: bad is not an integer')
    #     ]


def make_mock_node(node_id, mocker):
    node = mocker.Mock(autospec=True)
    node.name = 'node-%d' % node_id
    node.node_id = node_id
    return node
