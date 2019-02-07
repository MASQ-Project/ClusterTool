# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from command import Command

class TestCommand:

    def test_construction(self):
        subject = Command('Fred', run_it, 'the info')

        assert subject.name == 'Fred'
        assert subject.run() == 'I ran'
        assert subject.info == 'the info'

    def test_display(self, mocker):
        subject = Command('Fred', run_it, 'the info')
        mock_print = mocker.patch('__builtin__.print')
        subject.display()

        mock_print.assert_called_with("\tFred--------------> the info")

    def test_run_for_with_no_input(self, mocker):
        subject = Command('Fred', run_it, 'the info')
        mock_print = mocker.patch('__builtin__.print')
        result = subject.run_for('')

        mock_print.assert_not_called()
        assert result == 'I ran'

    def test_run_for_with_some_input(self, mocker):
        subject = Command('Fred', run_it, 'the info')
        mock_print = mocker.patch('__builtin__.print')
        result = subject.run_for('he-man')

        mock_print.assert_called_with("Fred command does not take input (yet?)")
        assert result == 'I ran'


def run_it():
    return 'I ran'
