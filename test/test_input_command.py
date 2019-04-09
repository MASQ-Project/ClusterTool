# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from command import InputCommand


class TestInputCommand:

    def test_construction(self):
        subject = InputCommand('Fred', run_it, 'the info')

        assert subject.name == 'Fred'
        assert subject.run('scissors') == 'I ran with scissors'
        assert subject.info == 'the info'

    def test_display(self, mocker):
        subject = InputCommand('Fred', run_it, 'the info')
        mock_print = mocker.patch('__builtin__.print')
        subject.display()

        mock_print.assert_called_with("\tFred--------------> the info")

    def test_run_for_with_no_input(self):
        subject = InputCommand('Fred', run_it, 'the info')
        result = subject.run_for('')

        assert result == 'I ran with '

    def test_run_for_with_some_input(self):
        subject = InputCommand('Fred', run_it, 'the info')
        result = subject.run_for('he-man')

        assert result == 'I ran with he-man'


def run_it(it):
    return 'I ran with ' + it
