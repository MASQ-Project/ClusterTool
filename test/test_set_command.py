# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
import pytest

import tnt_config
from command import SetCommand


class TestSetCommand:
    def setup_method(self, method):
        pass

    @pytest.fixture
    def instances(self, mocker):
        instance1 = mocker.Mock()
        instance1.attributes = {}
        instance2 = mocker.Mock()
        instance2.attributes = {}
        instance3 = mocker.Mock()
        instance3.attributes = {}
        mocker.patch.dict('tnt_config.INSTANCES', first=instance1, second=instance2, third=instance3)

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

        subject = SetCommand()

        subject.run_for('attribute value')

        assert tnt_config.INSTANCES['first'].attributes == {'attribute': 'value'}
        assert tnt_config.INSTANCES['second'].attributes == {}
        assert tnt_config.INSTANCES['third'].attributes == {}

    def test_all_when_prompted_finishes(self, instances,  mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.return_value = 'all'

        subject = SetCommand()

        subject.run_for('attribute value')

        assert tnt_config.INSTANCES['first'].attributes == {'attribute': 'value'}
        assert tnt_config.INSTANCES['second'].attributes == {'attribute': 'value'}
        assert tnt_config.INSTANCES['third'].attributes == {'attribute': 'value'}

    def test_run_for_specific_instances(self, instances):
        subject = SetCommand()

        subject.run_for('attribute value third first third')

        assert tnt_config.INSTANCES['first'].attributes == {'attribute': 'value'}
        assert tnt_config.INSTANCES['second'].attributes == {}
        assert tnt_config.INSTANCES['third'].attributes == {'attribute': 'value'}

    def test_run_for_all(self, instances):
        subject = SetCommand()

        subject.run_for('   attribute  value   all')

        assert tnt_config.INSTANCES['first'].attributes == {'attribute': 'value'}
        assert tnt_config.INSTANCES['second'].attributes == {'attribute': 'value'}
        assert tnt_config.INSTANCES['third'].attributes == {'attribute': 'value'}

    def test_complains_when_instance_is_not_known(self, instances, mocker):
        mock_input = mocker.patch('__builtin__.raw_input')
        mock_input.side_effect = ['first', '']
        mock_print = mocker.patch('__builtin__.print')

        subject = SetCommand()

        subject.run_for('attribute value notaninstance')

        mock_print.assert_called_with("\tno known instance called notaninstance")
        assert tnt_config.INSTANCES['first'].attributes == {'attribute': 'value'}
        assert tnt_config.INSTANCES['second'].attributes == {}
        assert tnt_config.INSTANCES['third'].attributes == {}
