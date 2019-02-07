# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import help as subject


class TestHelp:

    @pytest.fixture
    def printing(self, mocker):
        self.mock_print = mocker.patch('__builtin__.print', autospec=True)

    def test_name(self):
        assert subject.name() == 'help'

    def test_command_properties(self):
        real_command = subject.command()

        assert real_command.name == 'help'
        assert real_command.info == "shows usage information for specified command"

    def test_command(self, printing, mocker):
        real_command = subject.command()

        real_command.run_for('shell')

        assert self.mock_print.mock_calls == [
            mocker.call('\n', end=''),
            mocker.call('_unix-only_\n', end=''),
            mocker.call('\n', end=''),
            mocker.call('`shell` is a SelectCommand that will open a shell into the instance(s) specified in a new terminal window (per specified instance)\n', end=''),
            mocker.call('\n', end=''),
        ]

    def test_help_command_handles_nonexistent_command(self, printing, mocker):
        real_command = subject.command()

        real_command.run_for('booga')

        assert self.mock_print.mock_calls == [
            mocker.call("\nNo help available for command 'booga'\n"),
        ]

    def test_help_command_handles_last_command_in_file(self, printing, mocker):
        real_command = subject.command()
        last_documented_command = ''
        last_documentation = []
        with open('USAGE.md', 'rt') as usage_fh:
            while True:
                line = usage_fh.readline()
                if line == '':
                    break
                if line.startswith('### '):
                    last_documented_command = line[4:-1]
                    last_documentation = []
                else:
                    last_documentation.append(mocker.call(line, end=''))

        assert last_documented_command != '', 'No commands found in documentation file'

        real_command.run_for(last_documented_command)

        assert self.mock_print.mock_calls == last_documentation

    def test_help_command_prompts_for_target(self, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        real_command = subject.command()

        real_command.run_for('')

        mock_input.assert_called_with('Which command would you like help for? (blank to cancel) ')

