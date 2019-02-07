# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from finish import *


class TestFinish:

    @pytest.fixture
    def os(self, mocker):
        self.mock_os = mocker.patch('finish.os')

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print')

    @pytest.fixture
    def instances(self, mocker):
        self.mock_first_instance = mocker.Mock()
        self.mock_second_instance = mocker.Mock()
        mocker.patch.dict('command.INSTANCES', first=self.mock_first_instance, second=self.mock_second_instance)

    def test_name(self):
        assert name() == 'finish'

    def test_command(self, mocker, os, instances):
        real_command = command()

        assert real_command.name == 'finish'
        assert real_command.info == 'Prompts for destination dir(should not exist), `stop`(all) then download logs to dst dir for all running instances'

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.return_value = 'testdir'
        self.mock_os.path.exists.return_value = False

        real_command.run_for([])

        mock_input.assert_called_with('\tPlease enter a new directory name for the logs (blank line to cancel): ')
        self.mock_os.mkdir.assert_called_with('testdir')

        self.mock_first_instance.stop_node.assert_called_with()
        self.mock_first_instance.retrieve_logs.assert_called_with('testdir')

        self.mock_second_instance.stop_node.assert_called_with()
        self.mock_second_instance.retrieve_logs.assert_called_with('testdir')

    def test_command_sad_paths(self, mocker, os, printing, instances):
        real_command = command()

        assert real_command.name == 'finish'
        assert real_command.info == 'Prompts for destination dir(should not exist), `stop`(all) then download logs to dst dir for all running instances'

        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value.strip.side_effect = ['test dir', 'valid', '']
        self.mock_os.path.exists.side_effect = [True, False]

        real_command.run_for([])

        mock_input.assert_called_with('\tPlease enter a new directory name for the logs (blank line to cancel): ')

        assert self.mock_print.mock_calls == [
            mocker.call('\tERROR please no spaces, try again\n'),
            mocker.call('\tERROR valid already exists, try again\n')
        ]

        assert self.mock_os.mkdir.call_count == 0

        assert self.mock_first_instance.stop_node.call_count == 0
        assert self.mock_first_instance.retrieve_logs.call_count == 0

        assert self.mock_second_instance.stop_node.call_count == 0
        assert self.mock_second_instance.retrieve_logs.call_count == 0
