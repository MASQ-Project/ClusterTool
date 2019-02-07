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
        instance_dict = {'bootstrap': self.mock_bootstrap_instance, 'other': self.mock_other_instance}
        mocker.patch.object(subject, 'INSTANCES', instance_dict)

    @pytest.fixture
    def command_instances(self, mocker):
        self.mock_bootstrap_instance = mocker.Mock(autospec=True)
        self.mock_bootstrap_instance.name = 'bootstrap'
        self.mock_other_instance = mocker.Mock(autospec=True)
        self.mock_other_instance.name = 'other'
        instance_dict = {'bootstrap': self.mock_bootstrap_instance, 'other': self.mock_other_instance}
        mocker.patch.object(command, 'INSTANCES', instance_dict)

    def test_name(self):
        assert subject.name() == 'start'

    def test_command(self):
        real_command = subject.command()

        assert real_command.name == 'start'
        assert real_command.info == 'starts SubstratumNode on'

    def test_command_with_bootstrap(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.return_value = 'bootstrap'
        real_command = subject.command()

        real_command.run_for('bootstrap')

        assert self.mock_bootstrap_instance.start_node.call_count == 0

    def test_command_when_not_trying_to_start_node_on_bootstrap_and_node_is_running_on_bootstrap(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.return_value = 'other'
        self.mock_bootstrap_instance.node.descriptor = 'descriptor'
        real_command = subject.command()

        real_command.run_for('other')

        self.mock_other_instance.start_node.assert_called_with('descriptor')

    def test_command_when_trying_to_start_node_on_bootstrap_and_node_is_not_running_on_bootstrap(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.return_value = 'bootstrap'
        self.mock_bootstrap_instance.node.descriptor = ''
        real_command = subject.command()

        real_command.run_for('bootstrap')

        self.mock_bootstrap_instance.start_node.assert_called_with()

    def test_command_failure_to_start(self, mocker, printing, command_instances):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.return_value = 'other'
        real_command = subject.command()

        real_command.run_for('other')

        assert self.mock_print.mock_calls == [
            mocker.call('FAILED TO START other: did you forget about the bootstrap node?'),
            mocker.call('\t(if you are trying to start the bootstrap node, this means it may already be running)')
        ]
