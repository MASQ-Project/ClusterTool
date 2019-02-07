# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import runner as subject


class TestRunner:

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print', autospec=True)

    @pytest.fixture
    def instances(self, mocker):
        self.mock_first_instance = mocker.Mock()
        self.mock_second_instance = mocker.Mock()
        mocker.patch.dict('runner.INSTANCES', first=self.mock_first_instance, second=self.mock_second_instance)

    def test_go_with_valid_user_command(self, printing, mocker, instances):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = [' valid ', '', 'Y']
        subject.COMMANDS = {
            'init': mocker.Mock(autospec=True),
            'info': mocker.Mock(autospec=True),
            'valid': mocker.Mock(autospec=True)
        }

        subject.go()

        subject.COMMANDS['init'].display.assert_called_with()
        subject.COMMANDS['info'].display.assert_called_with()
        subject.COMMANDS['valid'].display.assert_called_with()
        subject.COMMANDS['init'].run.assert_called_with()
        subject.COMMANDS['info'].run.assert_called_with()
        subject.COMMANDS['valid'].run_for.assert_called_with('')
        assert self.mock_print.mock_calls == [
            mocker.call('available commands:'),
            mocker.call('only one per line, all lower case'),
            mocker.call('blank line to exit\n'),
            mocker.call('valid done'),
            mocker.call("commands: ['info', 'init', 'valid'], (blank line to exit)")
        ]

        assert mock_input.mock_calls == [
            mocker.call(),
            mocker.call('\n'),
            mocker.call('It looks like there are instances still running. Are you sure you want to exit? [y/N] ')
        ]

    def test_go_with_invalid_user_command(self, printing, mocker, instances):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = [' invalid ', '', 'Y']
        subject.COMMANDS = {
            'init': mocker.Mock(autospec=True),
            'info': mocker.Mock(autospec=True),
            'valid': mocker.Mock(autospec=True)
        }

        subject.go()

        subject.COMMANDS['init'].display.assert_called_with()
        subject.COMMANDS['info'].display.assert_called_with()
        subject.COMMANDS['valid'].display.assert_called_with()
        subject.COMMANDS['init'].run.assert_called_with()
        subject.COMMANDS['info'].run.assert_called_with()
        assert self.mock_print.mock_calls == [
            mocker.call('available commands:'),
            mocker.call('only one per line, all lower case'),
            mocker.call('blank line to exit\n'),
            mocker.call('unrecognized command: invalid'),
            mocker.call('available commands:'),
            mocker.call('only one per line, all lower case'),
            mocker.call('blank line to exit\n'),
            mocker.call('invalid done'),
            mocker.call("commands: ['info', 'init', 'valid'], (blank line to exit)")
        ]

        assert mock_input.mock_calls == [
            mocker.call(),
            mocker.call('\n'),
            mocker.call('It looks like there are instances still running. Are you sure you want to exit? [y/N] ')
        ]

    def test_go_not_sure_on_exit(self, printing, mocker, instances):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['', 'N', '', 'Y', '']
        subject.COMMANDS = {
            'init': mocker.Mock(autospec=True),
            'info': mocker.Mock(autospec=True),
            'test': mocker.Mock(autospec=True)
        }

        subject.go()

        subject.COMMANDS['init'].display.assert_called_with()
        subject.COMMANDS['info'].display.assert_called_with()
        subject.COMMANDS['init'].run.assert_called_with()
        subject.COMMANDS['info'].run.assert_called_with()
        assert self.mock_print.mock_calls == [
            mocker.call('available commands:'),
            mocker.call('only one per line, all lower case'),
            mocker.call('blank line to exit\n'),
            mocker.call(''),
            mocker.call("commands: ['info', 'test', 'init'], (blank line to exit)"),
            mocker.call('')
        ]

        assert mock_input.mock_calls == [
            mocker.call(),
            mocker.call('It looks like there are instances still running. Are you sure you want to exit? [y/N] '),
            mocker.call(),
            mocker.call('It looks like there are instances still running. Are you sure you want to exit? [y/N] ')
        ]

    def test_go_without_instances(self, printing, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['']
        subject.COMMANDS = {'init': mocker.Mock(autospec=True), 'info': mocker.Mock(autospec=True)}

        subject.go()

        assert self.mock_print.mock_calls == [
            mocker.call("You haven't configured any nodes for this run of TNT. Exiting...")
        ]
