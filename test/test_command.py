# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from command import Command, SetCommand
import tnt_config

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

    def test_couple_of_set_commands(self, mocker):
        subject = SetCommand()
        instance1 = mocker.Mock()
        instance1.configure_mock(attributes={})
        instance2 = mocker.Mock()
        instance2.configure_mock(attributes={})
        instance3 = mocker.Mock()
        instance3.configure_mock(attributes={})
        tnt_config.INSTANCES = {
            'node-0': instance1,
            'node-1': instance2,
            'node-2': instance3,
        }

        result1 = subject.run_for('attribute1 value1 node-0 node-1')
        result2 = subject.run_for('attribute2 value2 node-2')

        assert subject.name == 'set'
        assert tnt_config.INSTANCES['node-0'].attributes == {'attribute1': 'value1'}
        assert tnt_config.INSTANCES['node-1'].attributes == {'attribute1': 'value1'}
        assert tnt_config.INSTANCES['node-2'].attributes == {'attribute2': 'value2'}

def run_it():
    return 'I ran'
