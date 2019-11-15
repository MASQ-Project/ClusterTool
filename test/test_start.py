# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import command
import start as subject


class TestStart:

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print', autospec=True)

    @pytest.fixture
    def instances(self, mocker, command_instances):
        instance_dict = {'node-0': self.mock_node0, 'other': self.mock_other_instance}
        mocker.patch.object(subject, 'INSTANCES', instance_dict)

    @pytest.fixture
    def command_instances(self, mocker):
        self.mock_node0 = mocker.Mock(autospec=True)
        self.mock_node0.name = 'node-0'
        self.mock_other_instance = mocker.Mock(autospec=True)
        self.mock_other_instance.name = 'other'
        instance_dict = {'node-0': self.mock_node0, 'other': self.mock_other_instance}
        mocker.patch.object(command, 'INSTANCES', instance_dict)

    def test_name(self):
        assert subject.name() == 'start'

    def test_command(self):
        real_command = subject.command()

        assert real_command.name == 'start'
        assert real_command.info == 'starts MASQNode on'

    def test_command_with_node0(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.return_value = 'node-0'
        real_command = subject.command()

        real_command.run_for('node-0')

        assert self.mock_node0.start_node.call_count == 0

    def test_command_when_not_trying_to_start_node_on_node0_and_node_is_running_on_node0(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.return_value = 'other'
        self.mock_node0.node.descriptor = 'descriptor'
        real_command = subject.command()

        real_command.run_for('other')

        self.mock_other_instance.start_node.assert_called_with('descriptor')

    def test_command_when_trying_to_start_node_on_node0_and_node_is_not_running_on_node0(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.return_value = 'node-0'
        self.mock_node0.node.descriptor = ''
        real_command = subject.command()

        real_command.run_for('node-0')

        self.mock_node0.start_node.assert_called_with()

    def test_command_failure_to_start(self, mocker, printing, command_instances):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.return_value = 'other'
        real_command = subject.command()

        real_command.run_for('other')

        assert self.mock_print.mock_calls == [
            mocker.call('FAILED TO START other: did you forget about node-0?'),
            mocker.call('\t(if you are trying to start node-0, this means it may already be running)')
        ]
