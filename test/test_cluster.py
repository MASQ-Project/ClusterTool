# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import cluster as subject


class TestCluster:

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print', autospec=True)

    @pytest.fixture
    def instances(self, mocker):
        self.mock_node0 = mocker.Mock(autospec=True)
        self.mock_node0.name = 'node-0'
        self.mock_node0.node_id = 0
        self.mock_node0.node.descriptor = ''
        self.mock_node1 = make_mock_instance(1, mocker)
        self.mock_node2 = make_mock_instance(2, mocker)
        self.mock_node3 = make_mock_instance(3, mocker)
        self.mock_node4 = make_mock_instance(4, mocker)
        self.mock_node5 = make_mock_instance(5, mocker)
        self.mock_node6 = make_mock_instance(6, mocker)
        self.mock_node7 = make_mock_instance(7, mocker)

        instance_dict = {
            'node-0': self.mock_node0,
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

    def test_command_for_three_nodes_and_node0_is_not_running(self, instances):
        self.mock_node0.start_node.return_value = 'descriptor'

        real_command = subject.command()

        real_command.run_for('3')

        self.mock_node0.start_node.assert_called_with()
        self.mock_node1.start_node.assert_called_with('descriptor')
        self.mock_node2.start_node.assert_called_with('descriptor')
        self.mock_node3.start_node.assert_called_with('descriptor')
        self.mock_node4.start_node.assert_not_called()

    def test_command_for_three_nodes_and_node0_is_already_running(self, instances):
        self.mock_node0.node.descriptor = 'node-0-descriptor'

        real_command = subject.command()

        real_command.run_for('3')

        self.mock_node0.start_node.assert_not_called()
        self.mock_node1.start_node.assert_called_with('node-0-descriptor')
        self.mock_node2.start_node.assert_called_with('node-0-descriptor')
        self.mock_node3.start_node.assert_called_with('node-0-descriptor')
        self.mock_node4.start_node.assert_not_called()

    def test_command_for_two_clusters_and_node0_is_not_running(self, instances):
        self.mock_node0.start_node.return_value = 'mock-descriptor'
        self.mock_node3.start_node.return_value = 'mock-3-descriptor'

        real_command = subject.command()

        real_command.run_for('3')

        self.mock_node0.start_node.assert_called_with()
        self.mock_node1.start_node.assert_called_with('mock-descriptor')
        self.mock_node2.start_node.assert_called_with('mock-descriptor')
        self.mock_node3.start_node.assert_called_with('mock-descriptor')
        self.mock_node4.start_node.assert_not_called()

        self.mock_node0.reset_mock()
        self.mock_node3.reset_mock()
        self.mock_node0.node.descriptor = 'mock-descriptor'
        set_descriptor(self.mock_node1, 'mock-1-descriptor')
        set_descriptor(self.mock_node2, 'mock-2-descriptor')
        set_descriptor(self.mock_node3, 'mock-3-descriptor')

        real_command.run_for('3')

        self.mock_node0.start_node.assert_not_called()
        self.mock_node3.start_node.assert_not_called()
        self.mock_node4.start_node.assert_called_with('mock-3-descriptor')
        self.mock_node5.start_node.assert_called_with('mock-3-descriptor')
        self.mock_node6.start_node.assert_called_with('mock-3-descriptor')
        self.mock_node7.start_node.assert_not_called()

    def test_command_with_bad_count(self, mocker, printing, instances):
        real_command = subject.command()

        real_command.run_for('bad')

        assert self.mock_print.mock_calls == [
            mocker.call('FAILED TO START cluster: bad is not an integer')
        ]


def make_mock_instance(node_id, mocker):
    instance = mocker.Mock(autospec=True)
    instance._index_name = 'node-%d' % node_id
    instance.node_id = node_id
    instance.node.descriptor = ''
    return instance

def set_descriptor(instance, descriptor):
    instance.start_node.return_value = descriptor
    instance.node.descriptor = descriptor