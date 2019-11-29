# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
import tnt_config
from command import SelectCommand


class TestSelectCommand:

    @pytest.fixture
    def instances(self, mocker):
        tnt_config.INSTANCES = {'first': 'Anakin', 'second': 'Obi-Wan', 'third': 'Ahsoka'}

    def test_construction(self):
        def run_it():
            return 'I ran'
        subject = SelectCommand('Bob', run_it, 'greets')

        assert subject.name == 'Bob'
        assert subject.info == 'greets'
        assert subject.sub_fn() == 'I ran'

    def test_display(self, mocker):
        subject = SelectCommand('Bob', None, 'greets')
        mock_print = mocker.patch('__builtin__.print')
        subject.display()

        mock_print.assert_called_with("\tBob---------------> Prompts for instance name then greets the instance(s) specified")

    def test_run_for_with_no_input_will_prompt(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['first', '']
        ran_for = []

        def run_for(whom):
            ran_for.append(whom)
        subject = SelectCommand('Bob', run_for, 'greets')

        subject.run_for('')

        assert ran_for == ['Anakin']

    def test_all_when_prompted_finishes(self, instances,  mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value = 'all'
        ran_for = []

        def run_for(whom):
            ran_for.append(whom)
        subject = SelectCommand('Bob', run_for, 'greets')

        subject.run_for('')

        assert ran_for == [
            'Anakin',
            'Obi-Wan',
            'Ahsoka'
        ]

    def test_run_for_specific_instances(self, instances):
        ran_for = []

        def run_for(whom):
            ran_for.append(whom)
        subject = SelectCommand('Bob', run_for, 'greets')

        subject.run_for('third first third')

        assert ran_for == [
            'Anakin',
            'Ahsoka'
        ]

    def test_run_for_all(self, instances):
        ran_for = []

        def run_for(whom):
            ran_for.append(whom)
        subject = SelectCommand('Bob', run_for, 'greets')

        subject.run_for('   all')

        assert ran_for == [
            'Anakin',
            'Obi-Wan',
            'Ahsoka'
        ]

    def test_complains_when_instance_is_not_known(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['first', '']
        mock_print = mocker.patch('__builtin__.print')

        ran_for = []

        def run_for(whom):
            ran_for.append(whom)
        subject = SelectCommand('Bob', run_for, 'greets')

        subject.run_for('notaninstance')

        mock_print.assert_called_with("\tno known instance called notaninstance")
        assert ran_for == ['Anakin']
