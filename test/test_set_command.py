# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest
from command import SetCommand

class InstanceForTest:
    def __init__(self):
        self.attributes = {}

class TestSetCommand:
    def setup_method(self, method):
        self.first = InstanceForTest()
        self.second = InstanceForTest()
        self.third = InstanceForTest()

    @pytest.fixture
    def instances(self, mocker):
        mocker.patch.dict('command.INSTANCES', first=self.first, second=self.second, third=self.third)

    def test_construction(self):
        subject = SetCommand()

        assert subject.name == 'set'
        assert subject.info == 'sets attributes on a Node before it is started'
        assert subject.sub_fn() == 0

    def test_display(self, mocker):
        subject = SetCommand()
        mock_print = mocker.patch('__builtin__.print')
        subject.display()

        mock_print.assert_called_with("\tset---------------> Prompts for instance name then sets an attribute on the instance(s) specified")

    def test_run_for_with_no_input_will_prompt(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['first', '']

        def run_for(whom):
            ran_for.append(whom)
        subject = SetCommand()

        subject.run_for('attribute value')

        assert self.first.attributes == {'attribute': 'value'}
        assert self.second.attributes == {}
        assert self.third.attributes == {}

    def test_all_when_prompted_finishes(self, instances,  mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value = 'all'

        subject = SetCommand()

        subject.run_for('attribute value')

        assert self.first.attributes == {'attribute': 'value'}
        assert self.second.attributes == {'attribute': 'value'}
        assert self.third.attributes == {'attribute': 'value'}

    def test_run_for_specific_instances(self, instances):
        subject = SetCommand()

        subject.run_for('attribute value third first third')

        assert self.first.attributes == {'attribute': 'value'}
        assert self.second.attributes == {}
        assert self.third.attributes == {'attribute': 'value'}

    def test_run_for_all(self, instances):
        subject = SetCommand()

        subject.run_for('   attribute  value   all')

        assert self.first.attributes == {'attribute': 'value'}
        assert self.second.attributes == {'attribute': 'value'}
        assert self.third.attributes == {'attribute': 'value'}

    def test_complains_when_instance_is_not_known(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['first', '']
        mock_print = mocker.patch('__builtin__.print')

        subject = SetCommand()

        subject.run_for('attribute value notaninstance')

        mock_print.assert_called_with("\tno known instance called notaninstance")
        assert self.first.attributes == {'attribute': 'value'}
        assert self.second.attributes == {}
        assert self.third.attributes == {}
